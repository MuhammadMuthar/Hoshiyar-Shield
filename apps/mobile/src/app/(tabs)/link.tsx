import * as Clipboard from 'expo-clipboard';
import { router } from 'expo-router';
import { ClipboardPaste, EyeOff, Flag, Globe, Search } from 'lucide-react-native';
import { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { RiskBadge } from '../../components/RiskBadge';
import { Screen } from '../../components/Screen';
import { Txt } from '../../components/Txt';
import { Chip, EmptyState, Field, Notice, SectionHeader } from '../../components/bits';
import { analyzeUrl, type UrlAnalysis } from '../../engine/url';
import { addHistory } from '../../features/history';
import { usePreferences } from '../../features/preferences';
import { colors, font, riskStyle } from '../../theme';

const DEMO_LINKS = ['http://jazzcash-verify.example/login', 'https://easypaesa.com/claim', 'https://www.hbl.com@account-update.example', 'https://www.jazzcash.com.pk'];
function shortLink(u: string) {
  const t = u.replace(/^https?:\/\//, '');
  return t.length > 26 ? t.slice(0, 25) + '…' : t;
}
const SEV = { high: colors.red, medium: colors.amber, low: colors.sky, info: colors.textDim } as const;

export default function LinkCheck() {
  const prefs = usePreferences();
  const [input, setInput] = useState('');
  const [result, setResult] = useState<UrlAnalysis | null>(null);
  const [error, setError] = useState<string | undefined>();

  const check = (value = input) => {
    const r = analyzeUrl(value);
    if (!r.ok) {
      setError(r.message);
      setResult(null);
      return;
    }
    setError(undefined);
    setResult(r);
    void addHistory({ kind: 'link', level: r.level, preview: r.parsed.host }, prefs.saveHistory);
  };

  const rs = result ? riskStyle[result.level] : null;
  return (
    <Screen title="Check a Link" subtitle="Structural analysis. We never open the link." testID="link-screen">
      <Field
        testID="link-input"
        label="Link (URL)"
        value={input}
        onChangeText={(t) => { setInput(t); setError(undefined); }}
        placeholder="e.g. http://jazzcash-verify.example/login"
        autoCapitalize="none"
        autoCorrect={false}
        keyboardType="url"
        returnKeyType="search"
        onSubmitEditing={() => check()}
        error={error}
      />
      <View style={{ flexDirection: 'row', gap: 10 }}>
        <Button label="Check link" icon={Search} onPress={() => check()} disabled={!input.trim()} style={{ flex: 1 }} testID="check-link" />
        <Button
          label="Paste"
          icon={ClipboardPaste}
          variant="secondary"
          onPress={async () => {
            const clip = await Clipboard.getStringAsync().catch(() => '');
            if (clip.trim()) { setInput(clip.trim()); check(clip.trim()); } else setError('Clipboard is empty.');
          }}
        />
      </View>
      {prefs.demoMode ? (
        <View style={styles.chips}>
          {DEMO_LINKS.map((l) => (
            <Chip key={l} label={shortLink(l)} onPress={() => { setInput(l); check(l); }} />
          ))}
        </View>
      ) : null}

      {result && rs ? (
        <View style={{ gap: 14 }} testID="link-result">
          <Card style={{ gap: 10, borderColor: rs.color + '88', backgroundColor: rs.soft }}>
            <RiskBadge level={result.level} />
            <Txt variant="caption">Real destination (host)</Txt>
            <Txt style={{ fontFamily: font.bold, fontSize: 20, color: colors.text }} selectable>{result.parsed.host}</Txt>
            <Txt variant="small">
              Registered domain: <Txt variant="small" style={{ color: colors.text, fontFamily: font.bold }}>{result.parsed.registrableDomain}</Txt>
              {result.parsed.scheme ? `  ·  ${result.parsed.scheme}://` : ''}
            </Txt>
          </Card>
          <SectionHeader title={result.cues.length ? 'What we found' : 'Checks'} />
          <Card style={{ gap: 12 }}>
            {result.cues.length ? (
              result.cues.map((c) => (
                <View key={c.id} style={{ flexDirection: 'row', gap: 10 }}>
                  <View style={[styles.dot, { backgroundColor: SEV[c.severity] }]} />
                  <View style={{ flex: 1 }}>
                    <Txt variant="bodyStrong">{c.label}</Txt>
                    <Txt variant="small">{c.detail}</Txt>
                  </View>
                </View>
              ))
            ) : (
              <Txt variant="small">No structural warning signs found in this link.</Txt>
            )}
          </Card>
          <SectionHeader title="What to do" />
          <Card style={{ gap: 8 }}>
            {result.recommendations.map((r) => <Txt key={r} variant="body" style={{ color: colors.text }}>• {r}</Txt>)}
          </Card>
          {result.level !== 'LOW' ? (
            <Button label="Report this link" icon={Flag} variant="secondary" onPress={() => router.push({ pathname: '/report', params: { target: result.parsed.input } })} />
          ) : null}
          <Notice icon={EyeOff} text="This is a structural check of the link's shape against a small reference list of official domains. It is not a database of known malicious sites, so a clean result does not prove a site is safe." />
        </View>
      ) : (
        !error && <EmptyState icon={Globe} title="Paste a link from a message" text="We'll show where it really leads and flag look-alike bank domains, hidden redirects and other phishing tricks." />
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  dot: { width: 10, height: 10, borderRadius: 5, marginTop: 6 },
});
