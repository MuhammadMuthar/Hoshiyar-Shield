import { Cpu, Database, Lock, ScanText, ShieldCheck, Sparkles, Trash, Users } from 'lucide-react-native';
import { Alert, StyleSheet, View } from 'react-native';

import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Logo } from '../components/Logo';
import { Screen } from '../components/Screen';
import { Txt } from '../components/Txt';
import { IconBadge, SectionHeader, ToggleRow } from '../components/bits';
import { getClassifier } from '../engine/analyze';
import { usePreferences } from '../features/preferences';
import { colors } from '../theme';

const PIPELINE = [
  { icon: ScanText, title: '1 · Normalise', text: 'Roman Urdu spellings, Urdu script, leetspeak (0TP, J@zzCash), links and numbers are put into one canonical form.' },
  { icon: Cpu, title: '2 · AI classifier', text: 'Character n-gram TF-IDF + logistic regression, trained in Python and running here on your phone.' },
  { icon: ShieldCheck, title: '3 · Warning cues', text: 'Deterministic checks for OTP/PIN requests, advance fees, safe-account and screen-sharing tricks, and suspicious links.' },
  { icon: Sparkles, title: '4 · Risk fusion', text: 'Explicit, tested rules combine the AI score and cues into High Risk / Suspicious / No Obvious Scam Detected.' },
];

export default function About() {
  const prefs = usePreferences();
  const clf = getClassifier();
  const meta = clf.model.metadata as { created_at?: string; trained_on?: string; test_summary?: Record<string, number>; disclaimer?: string; config?: string };
  const ts = meta.test_summary ?? {};
  const pct = (x?: number) => (typeof x === 'number' ? `${(x * 100).toFixed(1)}%` : 'n/a');

  return (
    <Screen title="About & Settings" back testID="about-screen">
      <Card style={styles.brand}>
        <Logo size={52} />
        <View style={{ flex: 1 }}>
          <Txt variant="h2">Hoshiyar Shield</Txt>
          <Txt variant="small">AI-assisted financial scam warnings for Pakistan. Built for AICON’26 by Mutahar & Uswa.</Txt>
        </View>
      </Card>

      <SectionHeader title="AI model on this phone" />
      <Card style={{ gap: 6 }} testID="model-info">
        <Row k="Model version" v={clf.version} />
        <Row k="Created" v={meta.created_at?.slice(0, 10) ?? 'n/a'} />
        <Row k="Features" v={`${clf.model.vocab.length.toLocaleString()} character n-grams (${meta.config ?? ''})`} />
        <Row k="Thresholds" v={`Suspicious ≥ ${clf.thresholds.suspicious} · High ≥ ${clf.thresholds.high}`} />
        <Row k="Training data" v={meta.trained_on ?? 'n/a'} />
        <Row k="Held-out test (ML only)" v={`recall ${pct(ts.recall_at_suspicious)} · false alarms ${pct(ts.fpr_at_suspicious)} · precision@High ${pct(ts.precision_at_high)}`} />
        <Txt variant="caption" style={{ marginTop: 6 }}>{meta.disclaimer}</Txt>
      </Card>

      <SectionHeader title="How a message is checked" />
      <View style={{ gap: 10 }}>
        {PIPELINE.map((p) => (
          <Card key={p.title} style={{ flexDirection: 'row', gap: 12 }}>
            <IconBadge icon={p.icon} color={colors.teal} bg={colors.tealSoft} size={38} />
            <View style={{ flex: 1, gap: 2 }}>
              <Txt variant="title">{p.title}</Txt>
              <Txt variant="small">{p.text}</Txt>
            </View>
          </Card>
        ))}
      </View>

      <SectionHeader title="Privacy" />
      <Card style={{ gap: 8 }}>
        <Txt variant="small" style={{ color: colors.text }}>• Messages are analysed on this phone. No message text is sent to any server.</Txt>
        <Txt variant="small" style={{ color: colors.text }}>• Hoshiyar has no SMS, contacts or call-log permissions and never reads messages automatically.</Txt>
        <Txt variant="small" style={{ color: colors.text }}>• Links are never opened. Reports stay on this phone.</Txt>
        <Txt variant="small" style={{ color: colors.text }}>• Recent checks are stored only if you turn them on below (short previews, not full messages).</Txt>
      </Card>

      <SectionHeader title="Settings" />
      <Card style={{ gap: 4 }}>
        <ToggleRow title="Save recent checks" text="Keep a short list of your last checks on this phone." value={prefs.saveHistory} onChange={(v) => prefs.update({ saveHistory: v })} testID="toggle-history" />
        <View style={styles.divider} />
        <ToggleRow title="Hackathon demo mode" text="Show the sample message library and fictional demo reputation records." value={prefs.demoMode} onChange={(v) => prefs.update({ demoMode: v })} testID="toggle-demo" />
      </Card>
      <Button
        label="Delete all data on this phone"
        icon={Trash}
        variant="ghost"
        onPress={() =>
          Alert.alert('Delete all Hoshiyar data?', 'This removes recent checks, your saved reports and settings from this phone.', [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Delete', style: 'destructive', onPress: () => void prefs.resetAll() },
          ])
        }
      />

      <SectionHeader title="Limitations" />
      <Card style={{ gap: 8 }}>
        <Txt variant="small">• Trained and evaluated on synthetic messages. Real-world accuracy has not been measured yet.</Txt>
        <Txt variant="small">• Cannot verify who sent a message or who owns a number, and cannot block payments in other apps.</Txt>
        <Txt variant="small">• “No Obvious Scam Detected” is not a guarantee. New scam styles may be missed.</Txt>
      </Card>

      <View style={styles.footer}>
        <IconBadge icon={Users} color={colors.textMuted} bg={colors.surfaceAlt} size={32} />
        <Txt variant="caption" style={{ flex: 1 }}>Team: Mutahar & Uswa · Built with AI pair-programmers (Claude & ChatGPT) under a documented collaboration agreement.</Txt>
      </View>
      <View style={styles.footer}>
        <IconBadge icon={Database} color={colors.textMuted} bg={colors.surfaceAlt} size={32} />
        <Txt variant="caption" style={{ flex: 1 }}>Demo numbers use the fictional 0399-555xxxx range; demo links use reserved .example domains.</Txt>
      </View>
      <View style={styles.footer}>
        <IconBadge icon={Lock} color={colors.textMuted} bg={colors.surfaceAlt} size={32} />
        <Txt variant="caption" style={{ flex: 1 }}>Decision support only: not a certified fraud-prevention or regulatory system.</Txt>
      </View>
    </Screen>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <View style={styles.row}>
      <Txt variant="caption" style={{ width: 118 }}>{k}</Txt>
      <Txt variant="small" style={{ flex: 1, color: colors.text }} selectable>{v}</Txt>
    </View>
  );
}

const styles = StyleSheet.create({
  brand: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  row: { flexDirection: 'row', gap: 8, paddingVertical: 3 },
  divider: { height: 1, backgroundColor: colors.border, marginVertical: 6 },
  footer: { flexDirection: 'row', gap: 10, alignItems: 'center' },
});
