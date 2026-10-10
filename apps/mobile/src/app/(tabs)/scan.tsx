import * as Clipboard from 'expo-clipboard';
import { router, useLocalSearchParams } from 'expo-router';
import { ClipboardPaste, Cpu, Lock, Sparkles, X } from 'lucide-react-native';
import { useEffect, useState } from 'react';
import { Animated, Easing, Pressable, ScrollView, StyleSheet, TextInput, View } from 'react-native';

import samplesJson from '../../../assets/model/demo-samples.json';
import { Button } from '../../components/Button';
import { Screen } from '../../components/Screen';
import { Txt } from '../../components/Txt';
import { Notice, SectionHeader } from '../../components/bits';
import { AnalysisInputError, analyzeMessage, MAX_CHARS } from '../../engine/analyze';
import { addHistory } from '../../features/history';
import { usePreferences } from '../../features/preferences';
import { setCurrentAnalysis } from '../../features/session';
import { strings } from '../../i18n';
import { colors, font, isRtl, radius } from '../../theme';

interface Sample { id: string; title: string; language: string; example_of: string; text: string }
const SAMPLES = (samplesJson as { samples: Sample[] }).samples;
const LANG_LABEL: Record<string, string> = { roman_urdu: 'Roman Urdu', urdu: 'اردو', english: 'English', mixed: 'Mixed' };

export default function Scan() {
  const s = strings();
  const prefs = usePreferences();
  const params = useLocalSearchParams<{ text?: string }>();
  const [text, setText] = useState('');
  const [source, setSource] = useState<'typed' | 'pasted' | 'sample'>('typed');
  const [sampleId, setSampleId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const sweep = useState(() => new Animated.Value(0))[0];

  // Deep link: hoshiyar://scan?text=... pre-fills the box (never auto-analyses).
  const [seenParam, setSeenParam] = useState<string | undefined>();
  if (typeof params.text === 'string' && params.text.trim() && params.text !== seenParam) {
    setSeenParam(params.text);
    setText(params.text.slice(0, MAX_CHARS));
    setSource('pasted');
  }

  useEffect(() => {
    if (!busy) return;
    sweep.setValue(0);
    const loop = Animated.loop(Animated.timing(sweep, { toValue: 1, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: true }));
    loop.start();
    return () => loop.stop();
  }, [busy, sweep]);

  const paste = async () => {
    try {
      const clip = await Clipboard.getStringAsync();
      if (!clip.trim()) {
        setError('Your clipboard is empty. Copy the message first, then tap Paste.');
        return;
      }
      setText(clip.slice(0, MAX_CHARS));
      setSource('pasted');
      setSampleId(undefined);
      setError(null);
    } catch {
      setError("Couldn't read the clipboard. Long-press inside the box and choose Paste instead.");
    }
  };

  const analyse = () => {
    setError(null);
    let result;
    try {
      result = analyzeMessage(text);
    } catch (e) {
      setError(e instanceof AnalysisInputError ? e.message : 'Something went wrong while analysing. Please try again.');
      return;
    }
    setBusy(true);
    // The analysis itself is already done (a few ms on-device). This short
    // pause only lets the user see that a check happened. The real time is shown on the result.
    setTimeout(() => {
      setCurrentAnalysis({ text, result, source, sampleId });
      void addHistory({ kind: 'message', level: result.level, preview: text.replace(/\s+/g, ' ').trim() }, prefs.saveHistory);
      setBusy(false);
      router.push('/result');
    }, 650);
  };

  const chars = text.length;
  return (
    <Screen
      title={s.scanMessage}
      subtitle="Paste a suspicious SMS or WhatsApp message"
      testID="scan-screen"
      footer={<Button label={busy ? 'Analysing on-device…' : s.analyze} icon={Sparkles} onPress={analyse} disabled={!text.trim() || busy} loading={busy} size="lg" testID="analyse-button" />}
    >
      <View style={[styles.inputWrap, error ? { borderColor: colors.red } : null]}>
        <TextInput
          testID="message-input"
          accessibilityLabel="Message to analyse"
          value={text}
          onChangeText={(t) => {
            setText(t.slice(0, MAX_CHARS));
            setSource('typed');
            setSampleId(undefined);
            if (error) setError(null);
          }}
          placeholder={'Paste or type the message here…\n\ne.g. "Mubarak ho! Apka inaam nikla hai…"'}
          placeholderTextColor={colors.textDim}
          multiline
          textAlignVertical="top"
          selectionColor={colors.emerald}
          style={[styles.input, isRtl(text) && { writingDirection: 'rtl', textAlign: 'right' }]}
        />
        {busy ? (
          <Animated.View pointerEvents="none" style={[styles.sweep, { transform: [{ translateY: sweep.interpolate({ inputRange: [0, 1], outputRange: [0, 190] }) }] }]} />
        ) : null}
        <View style={styles.inputBar}>
          <Pressable accessibilityRole="button" accessibilityLabel={s.paste} onPress={paste} style={styles.smallBtn} testID="paste-button">
            <ClipboardPaste size={16} color={colors.emeraldBright} />
            <Txt style={styles.smallBtnText}>{s.paste}</Txt>
          </Pressable>
          {text ? (
            <Pressable accessibilityRole="button" accessibilityLabel={s.clear} onPress={() => { setText(''); setError(null); }} style={styles.smallBtn} testID="clear-button">
              <X size={16} color={colors.textMuted} />
              <Txt style={[styles.smallBtnText, { color: colors.textMuted }]}>{s.clear}</Txt>
            </Pressable>
          ) : null}
          <View style={{ flex: 1 }} />
          <Txt variant="caption" accessibilityLabel={`${chars} characters`}>{chars.toLocaleString()} / {MAX_CHARS.toLocaleString()}</Txt>
        </View>
      </View>
      {error ? <Txt variant="small" style={{ color: colors.redBright }} accessibilityLiveRegion="polite">{error}</Txt> : null}

      <View style={styles.privacy}>
        <Lock size={14} color={colors.emeraldBright} />
        <Txt variant="caption" style={{ flex: 1, color: colors.textMuted }}>{s.privacyOnDevice} Nothing is saved unless you turn on recent checks.</Txt>
      </View>

      {prefs.demoMode ? (
        <>
          <SectionHeader title="Demo library: tap to load a sample" />
          <Txt variant="small" style={{ marginTop: -8 }}>
            Original, fictional messages. Loading one only fills the box. You still press Analyse, and it runs through the same AI as your own messages.
          </Txt>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 10, paddingRight: 18 }} style={{ marginHorizontal: -18, paddingLeft: 18 }}>
            {SAMPLES.map((smp) => (
              <Pressable
                key={smp.id}
                testID={`sample-${smp.id}`}
                accessibilityRole="button"
                accessibilityLabel={`Load sample: ${smp.example_of}`}
                onPress={() => { setText(smp.text); setSource('sample'); setSampleId(smp.id); setError(null); }}
                style={[styles.sample, sampleId === smp.id && { borderColor: colors.emerald, backgroundColor: colors.emeraldSoft }]}
              >
                <Txt variant="caption" style={{ color: colors.emeraldBright }}>{LANG_LABEL[smp.language] ?? smp.language}</Txt>
                <Txt variant="title" numberOfLines={1}>{smp.title}</Txt>
                <Txt variant="caption" numberOfLines={2}>{smp.example_of}</Txt>
              </Pressable>
            ))}
          </ScrollView>
        </>
      ) : (
        <Notice icon={Cpu} text="Tip: copy a message from your SMS app, then tap Paste. Analysis works without internet." />
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  inputWrap: { borderRadius: radius.lg, borderWidth: 1, borderColor: colors.borderStrong, backgroundColor: colors.surface, overflow: 'hidden' },
  input: { minHeight: 200, maxHeight: 340, padding: 16, color: colors.text, fontFamily: font.medium, fontSize: 16, lineHeight: 24 },
  sweep: { position: 'absolute', left: 0, right: 0, top: 0, height: 3, backgroundColor: colors.emeraldBright, opacity: 0.8 },
  inputBar: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 10, paddingVertical: 8, borderTopWidth: 1, borderTopColor: colors.border, backgroundColor: colors.surfaceAlt },
  smallBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 7, borderRadius: radius.sm, backgroundColor: colors.surface },
  smallBtnText: { fontFamily: font.semibold, fontSize: 13, color: colors.emeraldBright },
  privacy: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  sample: { width: 168, gap: 4, padding: 12, borderRadius: radius.md, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.surface },
});
