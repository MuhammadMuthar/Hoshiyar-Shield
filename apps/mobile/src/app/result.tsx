import * as Haptics from 'expo-haptics';
import { router } from 'expo-router';
import { Brain, ChevronDown, ChevronUp, Cpu, Flag, Link2, ListChecks, ScanText, TriangleAlert } from 'lucide-react-native';
import { useEffect, useState } from 'react';
import { Animated, Pressable, StyleSheet, View } from 'react-native';

import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { CueList } from '../components/CueList';
import { RiskBadge } from '../components/RiskBadge';
import { Screen } from '../components/Screen';
import { ShieldMeter } from '../components/ShieldMeter';
import { Txt } from '../components/Txt';
import { EmptyState, SectionHeader } from '../components/bits';
import type { AnalysisResult } from '../engine/analyze';
import { useCurrentAnalysis } from '../features/session';
import { strings } from '../i18n';
import { colors, font, radius, riskStyle } from '../theme';

export default function Result() {
  const current = useCurrentAnalysis();
  const s = strings();
  const fade = useState(() => new Animated.Value(0))[0];
  const [showFull, setShowFull] = useState(false);
  const [showTech, setShowTech] = useState(false);

  useEffect(() => {
    if (!current) return;
    fade.setValue(0);
    Animated.timing(fade, { toValue: 1, duration: 450, delay: 150, useNativeDriver: true }).start();
    const lv = current.result.level;
    Haptics.notificationAsync(
      lv === 'HIGH' ? Haptics.NotificationFeedbackType.Error : lv === 'SUSPICIOUS' ? Haptics.NotificationFeedbackType.Warning : Haptics.NotificationFeedbackType.Success,
    ).catch(() => undefined);
  }, [current, fade]);

  if (!current) {
    return (
      <Screen title="Analysis" back>
        <EmptyState icon={ScanText} title="No message analysed yet" text="Paste a message on the Scan screen to see its risk assessment here." actionLabel={s.scanMessage} onAction={() => router.replace('/scan')} />
      </Screen>
    );
  }

  const { result: r, text } = current;
  const rs = riskStyle[r.level];
  const warnings = r.indicators.filter((i) => i.kind === 'action' || i.severity !== 'low');
  const other = r.indicators.filter((i) => !(i.kind === 'action' || i.severity !== 'low'));
  const reportTarget = r.phoneNumbers[0] ? '0' + r.phoneNumbers[0].replace('+92', '') : r.urls[0]?.parsed.host ?? '';
  const appear = { opacity: fade, transform: [{ translateY: fade.interpolate({ inputRange: [0, 1], outputRange: [16, 0] }) }] };

  return (
    <Screen
      title="Analysis"
      back
      testID="result-screen"
      footer={
        <View style={{ flexDirection: 'row', gap: 10 }}>
          <Button
            label="Report"
            icon={Flag}
            variant={r.level === 'LOW' ? 'secondary' : 'danger'}
            style={{ flex: 1 }}
            onPress={() => router.push({ pathname: '/report', params: { target: reportTarget, fromScan: '1' } })}
            testID="report-button"
          />
          <Button label={s.scanAnother} icon={ScanText} variant={r.level === 'LOW' ? 'primary' : 'secondary'} style={{ flex: 1.3 }} onPress={() => router.replace('/scan')} testID="scan-another" />
        </View>
      }
    >
      <View style={[styles.hero, { borderColor: rs.color + '66', backgroundColor: rs.soft }]}>
        <ShieldMeter level={r.level} score={r.ml.score} />
        <RiskBadge level={r.level} />
        <Txt variant="h1" align="center" testID="risk-title">{r.title}</Txt>
        <Txt variant="body" align="center" style={{ color: colors.text }}>{r.headline}</Txt>
        <View style={styles.metaRow}>
          <Cpu size={13} color={colors.textDim} />
          <Txt variant="caption">Analysed on this phone in {Math.max(1, Math.round(r.latencyMs))} ms · no internet used</Txt>
        </View>
      </View>

      <Animated.View style={[{ gap: 16 }, appear]}>
        {r.lowInformation ? (
          <Card tone="warning"><Txt variant="small" style={{ color: colors.text }}>This message is very short, so the AI has little to go on. Treat the result with extra caution.</Txt></Card>
        ) : null}

        <SectionHeader title="Message checked" />
        <Card>
          <Txt variant="bodyStrong" autoDirection numberOfLines={showFull ? undefined : 5}>{text}</Txt>
          {text.length > 220 ? (
            <Pressable onPress={() => setShowFull((v) => !v)} accessibilityRole="button" style={{ marginTop: 8 }}>
              <Txt variant="caption" style={{ color: colors.emeraldBright }}>{showFull ? 'Show less' : 'Show full message'}</Txt>
            </Pressable>
          ) : null}
        </Card>

        {warnings.length ? (
          <>
            <SectionHeader title={r.level === 'LOW' ? 'Things to keep in mind' : 'Warning signs found'} action={<Txt variant="caption">{warnings.length}</Txt>} />
            <CueList indicators={warnings} />
          </>
        ) : null}

        <SectionHeader title="What the AI model saw" />
        <ModelCard r={r} />

        {r.urls.length ? (
          <>
            <SectionHeader title="Links in this message" />
            {r.urls.map((u) => (
              <Card key={u.parsed.input} style={{ gap: 8 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                  <Link2 size={16} color={colors.textMuted} />
                  <Txt variant="bodyStrong" style={{ flex: 1 }} numberOfLines={1}>{u.parsed.host}</Txt>
                  <RiskBadge level={u.level} compact />
                </View>
                {u.cues.filter((c) => c.severity !== 'info').slice(0, 4).map((c) => (
                  <Txt key={c.id} variant="small">• {c.label}</Txt>
                ))}
                <Txt variant="caption">Structural check only. Hoshiyar never opens links.</Txt>
              </Card>
            ))}
          </>
        ) : null}

        <SectionHeader title="What you should do" />
        <Card style={{ gap: 12 }}>
          {r.recommendations.map((rec, i) => (
            <View key={rec} style={{ flexDirection: 'row', gap: 10 }}>
              <View style={[styles.stepNum, { backgroundColor: rs.soft, borderColor: rs.color }]}>
                <Txt style={{ fontFamily: font.bold, fontSize: 12, color: rs.bright }}>{i + 1}</Txt>
              </View>
              <Txt variant="body" style={{ flex: 1, color: colors.text }}>{rec}</Txt>
            </View>
          ))}
        </Card>

        {other.length ? (
          <>
            <SectionHeader title="Other observations" />
            <CueList indicators={other} />
          </>
        ) : null}

        <Pressable onPress={() => setShowTech((v) => !v)} accessibilityRole="button" style={styles.techToggle} testID="tech-toggle">
          <ListChecks size={16} color={colors.textMuted} />
          <Txt variant="bodyStrong" style={{ flex: 1 }}>Technical details</Txt>
          {showTech ? <ChevronUp size={18} color={colors.textMuted} /> : <ChevronDown size={18} color={colors.textMuted} />}
        </Pressable>
        {showTech ? (
          <Card tone="alt" style={{ gap: 6 }}>
            <Txt variant="mono">model: {r.ml.modelVersion}</Txt>
            <Txt variant="mono">ml score: {r.ml.score.toFixed(4)} → {r.ml.level}</Txt>
            <Txt variant="mono">thresholds: suspicious ≥ {r.ml.thresholds.suspicious}, high ≥ {r.ml.thresholds.high}</Txt>
            <Txt variant="mono">features matched: {r.ml.nFeatures}</Txt>
            <Txt variant="mono">latency: {r.latencyMs.toFixed(1)} ms (on-device)</Txt>
            {r.fusion.map((f) => <Txt key={f} variant="mono">{f}</Txt>)}
          </Card>
        ) : null}

        <View style={styles.disclaimer}>
          <TriangleAlert size={14} color={colors.textDim} />
          <Txt variant="caption" style={{ flex: 1 }}>
            {s.aiCanBeWrong} Hoshiyar is decision support, not a guarantee. It cannot verify who sent a message or block payments in other apps.
          </Txt>
        </View>
      </Animated.View>
    </Screen>
  );
}

function ModelCard({ r }: { r: AnalysisResult }) {
  const pct = Math.round(r.ml.score * 100);
  const words = r.level === 'LOW' ? r.ml.topLowering : r.ml.topRaising;
  const barColor = r.ml.level === 'HIGH' ? colors.red : r.ml.level === 'SUSPICIOUS' ? colors.amber : colors.emerald;
  return (
    <Card style={{ gap: 12 }}>
      <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
        <Brain size={18} color={colors.teal} />
        <Txt variant="title" style={{ flex: 1 }}>AI scam-pattern score</Txt>
        <Txt style={{ fontFamily: font.bold, fontSize: 16, color: barColor }}>{pct}/100</Txt>
      </View>
      <View style={styles.track} accessibilityLabel={`AI score ${pct} out of 100`}>
        <View style={[styles.fill, { width: `${Math.max(2, pct)}%`, backgroundColor: barColor }]} />
        <View style={[styles.tick, { left: `${r.ml.thresholds.suspicious * 100}%` }]} />
        <View style={[styles.tick, { left: `${r.ml.thresholds.high * 100}%` }]} />
      </View>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
        <Txt variant="caption">Legit-looking</Txt>
        <Txt variant="caption">Suspicious ≥ {Math.round(r.ml.thresholds.suspicious * 100)} · High ≥ {Math.round(r.ml.thresholds.high * 100)}</Txt>
      </View>
      {words.length ? (
        <>
          <Txt variant="small">
            {r.level === 'LOW' ? 'Words that made it look like a normal message:' : 'Words in this message that pushed the AI score up:'}
          </Txt>
          <View style={styles.words}>
            {words.map((w) => (
              <View key={w.token} style={[styles.word, { borderColor: (r.level === 'LOW' ? colors.emerald : barColor) + '88' }]}>
                <Txt style={{ fontFamily: font.semibold, fontSize: 13, color: colors.text }}>{w.token}</Txt>
              </View>
            ))}
          </View>
        </>
      ) : null}
      <Txt variant="caption">
        A model trained on Roman Urdu, Urdu and English examples produces this score from character patterns. It is a pattern-similarity score, not a probability that the message is a scam.
      </Txt>
    </Card>
  );
}

const styles = StyleSheet.create({
  hero: { alignItems: 'center', gap: 10, padding: 18, borderRadius: radius.xl, borderWidth: 1 },
  metaRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 2 },
  stepNum: { width: 24, height: 24, borderRadius: 12, alignItems: 'center', justifyContent: 'center', borderWidth: 1, marginTop: 1 },
  track: { height: 10, borderRadius: 5, backgroundColor: colors.surfaceHigh, overflow: 'hidden', justifyContent: 'center' },
  fill: { position: 'absolute', left: 0, top: 0, bottom: 0, borderRadius: 5 },
  tick: { position: 'absolute', width: 2, top: 0, bottom: 0, backgroundColor: colors.text, opacity: 0.6 },
  words: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  word: { paddingHorizontal: 10, paddingVertical: 5, borderRadius: radius.pill, borderWidth: 1, backgroundColor: colors.surfaceAlt },
  techToggle: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 10 },
  disclaimer: { flexDirection: 'row', gap: 8, alignItems: 'flex-start' },
});
