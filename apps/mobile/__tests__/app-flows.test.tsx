/**
 * UI flow tests: render the real Expo Router routes (src/app) and drive them
 * like a user. The analysis shown is produced by the real on-device model.
 */
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Clipboard from 'expo-clipboard';
import { act, fireEvent, renderRouter, screen, waitFor } from 'expo-router/testing-library';
import path from 'path';

import { setCurrentAnalysis } from '../src/features/session';

const APP = path.resolve(__dirname, '../src/app');
const SCAM = 'Mubarak ho! Apka 5 lakh ka inaam nikla hai. Inaam hasil karne ke liye 2,500 verification fee foran 0399-5550142 pe JazzCash karein.';

async function onboarded() {
  await AsyncStorage.setItem('hs.prefs.v1', JSON.stringify({ onboarded: true, saveHistory: false, demoMode: true }));
}

beforeEach(async () => {
  setCurrentAnalysis(null);
  await AsyncStorage.clear();
  jest.useRealTimers();
});

describe('navigation', () => {
  it('first launch shows onboarding, then Get Protected opens Home', async () => {
    const r = renderRouter(APP, { initialUrl: '/' });
    const cta = await screen.findByTestId('get-protected');
    expect(screen.getByText('Hoshiyar raho. Apna paisa bachao.')).toBeTruthy();
    fireEvent.press(cta);
    await screen.findByTestId('home-screen');
    expect(r.getPathname()).toBe('/home');
    expect(JSON.parse((await AsyncStorage.getItem('hs.prefs.v1')) ?? '{}').onboarded).toBe(true);
  });

  it('returning users land on Home with every primary action reachable', async () => {
    await onboarded();
    const r = renderRouter(APP, { initialUrl: '/' });
    await screen.findByTestId('home-screen');
    fireEvent.press(screen.getByTestId('home-scan'));
    await screen.findByTestId('scan-screen');
    expect(r.getPathname()).toBe('/scan');
  });
});

describe('scan → result', () => {
  it('analyses a typed Roman Urdu scam with the real model and shows HIGH risk', async () => {
    await onboarded();
    const r = renderRouter(APP, { initialUrl: '/scan' });
    const input = await screen.findByTestId('message-input');
    const fetchSpy = jest.spyOn(globalThis, 'fetch' as never);
    fireEvent.changeText(input, SCAM);
    fireEvent.press(screen.getByTestId('analyse-button'));
    await screen.findByTestId('result-screen', {}, { timeout: 3000 });
    expect(r.getPathname()).toBe('/result');
    expect(screen.getByTestId('risk-title').props.children).toBe('High Risk: possible financial scam');
    expect(screen.getByText('Fee demanded before a prize, loan or refund')).toBeTruthy();
    expect(fetchSpy).not.toHaveBeenCalled(); // on-device: no network
    fetchSpy.mockRestore();
  });

  it('a demo sample only fills the box; the legitimate alert comes back as no obvious scam', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/scan' });
    fireEvent.press(await screen.findByTestId('sample-demo-legit-alert'));
    expect(screen.getByTestId('message-input').props.value).toMatch(/^HBL: Your A\/C/);
    fireEvent.press(screen.getByTestId('analyse-button'));
    await screen.findByTestId('result-screen', {}, { timeout: 3000 });
    expect(screen.getByTestId('risk-title').props.children).toBe('No Obvious Scam Detected');
  });

  it('pastes from the clipboard', async () => {
    await onboarded();
    (Clipboard.getStringAsync as jest.Mock).mockResolvedValueOnce('Apna OTP foran share karein');
    renderRouter(APP, { initialUrl: '/scan' });
    fireEvent.press(await screen.findByTestId('paste-button'));
    await waitFor(() => expect(screen.getByTestId('message-input').props.value).toBe('Apna OTP foran share karein'));
  });

  it('disables analysis for empty input and handles long messages', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/scan' });
    const button = await screen.findByTestId('analyse-button');
    expect(button.props.accessibilityState?.disabled ?? screen.getByLabelText('Analyse message').props.accessibilityState.disabled).toBe(true);
    fireEvent.changeText(screen.getByTestId('message-input'), 'Bank ne kaha hai kabhi bhi apna OTP kisi ko na batayein. '.repeat(120));
    fireEvent.press(screen.getByTestId('analyse-button'));
    await screen.findByTestId('result-screen', {}, { timeout: 3000 });
  });

  it('result screen without an analysis shows a helpful empty state', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/result' });
    expect(await screen.findByText('No message analysed yet')).toBeTruthy();
  });
});

describe('link and number checks', () => {
  it('flags a brand look-alike link without opening it', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/link' });
    fireEvent.changeText(await screen.findByTestId('link-input'), 'http://jazzcash-verify.example/login');
    fireEvent.press(screen.getByTestId('check-link'));
    await screen.findByTestId('link-result');
    expect(screen.getAllByText('jazzcash-verify.example').length).toBeGreaterThan(0);
    expect(screen.getByText('HIGH RISK')).toBeTruthy();
  });

  it('normalises numbers, shows demo reports with caveats, and rejects invalid input', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/number' });
    const input = await screen.findByTestId('number-input');
    fireEvent.changeText(input, '12345');
    fireEvent.press(screen.getByTestId('check-number'));
    expect(await screen.findByText(/Pakistani mobile numbers start with 03/)).toBeTruthy();
    fireEvent.changeText(screen.getByTestId('number-input'), '+92 399 5550142');
    fireEvent.press(screen.getByTestId('check-number'));
    expect(await screen.findByText('3 reports describe suspicious prize-fee requests associated with this number.')).toBeTruthy();
    expect(screen.getByText(/synthetic DEMO records/)).toBeTruthy();
  });
});

describe('report flow', () => {
  it('validates, then saves a consented report locally without message text', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/report?target=0399-5550199' });
    fireEvent.press(await screen.findByTestId('save-report'));
    expect(await screen.findByText('Choose what kind of scam this was.')).toBeTruthy();
    fireEvent.press(screen.getByText('Prize / lottery fee'));
    fireEvent.press(screen.getByTestId('consent'));
    await act(async () => {
      fireEvent.press(screen.getByTestId('save-report'));
    });
    expect(await screen.findByText('Shukriya! Report saved.')).toBeTruthy();
    const saved = JSON.parse((await AsyncStorage.getItem('hs.reports.v1')) ?? '[]');
    expect(saved).toHaveLength(1);
    expect(saved[0]).toEqual(expect.objectContaining({ target: '+923995550199', category: 'prize_lottery', targetType: 'phone' }));
    expect(saved[0].messageText).toBeUndefined();
  });
});

describe('intelligence & about', () => {
  it('labels campaign data as simulated', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/intel' });
    expect(await screen.findByText(/SIMULATED DATA/)).toBeTruthy();
    expect(screen.getAllByText(/^C-0\d · /).length).toBeGreaterThan(3);
  });

  it('shows the model version on the technical info page', async () => {
    await onboarded();
    renderRouter(APP, { initialUrl: '/about' });
    await screen.findByTestId('model-info');
    expect(screen.getByText(/^hs-1\.0\.0\+/)).toBeTruthy();
  });
});
