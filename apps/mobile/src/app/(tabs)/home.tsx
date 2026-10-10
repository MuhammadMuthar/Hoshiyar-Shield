import { useFocusEffect, router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { ChevronRight, Clock, Cpu, Flag, Info, Lightbulb, Link2, Phone, Radar, ScanText, WifiOff } from 'lucide-react-native';
import { useMemo } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { Card } from '../../components/Card';
import { Logo } from '../../components/Logo';
import { RiskBadge } from '../../components/RiskBadge';
import { Screen } from '../../components/Screen';
import { Txt } from '../../components/Txt';
import { IconBadge, Notice, SectionHeader } from '../../components/bits';
import { getClassifier } from '../../engine/analyze';
import { useHistory } from '../../features/history';
import { usePreferences } from '../../features/preferences';
import { strings } from '../../i18n';
import { colors, font, radius } from '../../theme';

const TIPS = [
  'No bank, wallet or government office will ever ask for your OTP or PIN. Not on a call, not on SMS, not on WhatsApp.',
  'Genuine prizes and loans never ask you to pay a "verification", "tax" or "processing" fee first.',
  'Got a call from a "relative" on a new number asking for money? Call them back on their old number first.',
  'Money "sent by mistake"? Check your real balance in the official app before returning anything.',
  'Banks never ask you to move money to a "safe account". That is always a scam.',
  'Type your bank\'s website yourself or use the official app. Don\'t tap links in messages.',
];

export default function Home() {
  const prefs = usePreferences();
  const s = strings();
  const history = useHistory(prefs.saveHistory);
  useFocusEffect(history.refresh);
  const tip = useMemo(() => TIPS[new Date().getDate() % TIPS.length], []);
  const version = getClassifier().version;

  return (
    <Screen testID="home-screen">
      <View style={styles.top}>
        <Logo size={42} />
        <View style={{ flex: 1 }}>
          <Txt variant="h2">Hoshiyar Shield</Txt>
          <Txt variant="caption" style={{ color: colors.emeraldBright }}>{s.tagline}</Txt>
        </View>
        <Pressable accessibilityRole="button" accessibilityLabel="About the AI model and privacy" hitSlop={10} onPress={() => router.push('/about')} style={styles.iconBtn}>
          <Info size={20} color={colors.text} />
        </Pressable>
      </View>

      <Txt variant="h1">Assalam o Alaikum 👋</Txt>

      <Card tone="success" style={styles.status}>
        <View style={styles.pulse} />
        <View style={{ flex: 1, gap: 2 }}>
          <Txt variant="title">Shield ready on this phone</Txt>
          <Txt variant="small" style={{ color: colors.text }}>
            Paste any message you’re unsure about. Hoshiyar never reads your SMS on its own: you decide what to check.
          </Txt>
          <View style={styles.statusRow}>
            <View style={styles.pill}><Cpu size={12} color={colors.emeraldBright} /><Txt variant="caption" style={{ color: colors.emeraldBright }}>On-device AI</Txt></View>
            <View style={styles.pill}><WifiOff size={12} color={colors.emeraldBright} /><Txt variant="caption" style={{ color: colors.emeraldBright }}>Works offline</Txt></View>
          </View>
        </View>
      </Card>

      <Pressable accessibilityRole="button" accessibilityLabel={s.scanMessage} testID="home-scan" onPress={() => router.push('/scan')}>
        <LinearGradient colors={[colors.emerald, colors.teal]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={styles.primary}>
          <View style={styles.primaryIcon}><ScanText size={30} color={colors.bgDeep} strokeWidth={2.4} /></View>
          <View style={{ flex: 1 }}>
            <Txt style={{ fontFamily: font.extrabold, fontSize: 21, color: colors.bgDeep }}>{s.scanMessage}</Txt>
            <Txt style={{ fontFamily: font.medium, fontSize: 13, color: '#05332A' }}>SMS, WhatsApp or any text: Roman Urdu, اردو, English</Txt>
          </View>
          <ChevronRight size={24} color={colors.bgDeep} />
        </LinearGradient>
      </Pressable>

      <View style={styles.grid}>
        <Tile icon={Link2} title={s.checkLink} text="Spot fake bank sites" color={colors.teal} bg={colors.tealSoft} onPress={() => router.push('/link')} />
        <Tile icon={Phone} title={s.checkNumber} text="Before you pay" color={colors.amber} bg={colors.amberSoft} onPress={() => router.push('/number')} />
        <Tile icon={Flag} title={s.reportScam} text="Save a report" color={colors.redBright} bg={colors.redSoft} onPress={() => router.push('/report')} />
        <Tile icon={Radar} title="Scam trends" text="Campaign insights" color={colors.sky} bg={colors.skySoft} onPress={() => router.push('/intel')} />
      </View>

      {prefs.demoMode ? (
        <Notice text="Demo mode is on: sample messages and fictional reputation records are available for the presentation. Turn it off under About → Settings." />
      ) : null}

      <SectionHeader title="Recent checks" />
      {prefs.saveHistory ? (
        history.items.length ? (
          <Card padded={false}>
            {history.items.slice(0, 5).map((h, i) => (
              <View key={h.id} style={[styles.historyRow, i > 0 && { borderTopWidth: 1, borderTopColor: colors.border }]}>
                <Clock size={16} color={colors.textDim} />
                <View style={{ flex: 1 }}>
                  <Txt variant="bodyStrong" numberOfLines={1}>{h.preview}</Txt>
                  <Txt variant="caption">{h.kind} · {new Date(h.at).toLocaleString()}</Txt>
                </View>
                {h.level === 'HIGH' || h.level === 'SUSPICIOUS' || h.level === 'LOW' ? <RiskBadge level={h.level} compact /> : <Txt variant="caption">{h.level === 'REPORTED' ? 'Reported' : 'No reports'}</Txt>}
              </View>
            ))}
          </Card>
        ) : (
          <Card><Txt variant="small">No checks yet. Your next scans will appear here (stored only on this phone).</Txt></Card>
        )
      ) : (
        <Card>
          <Txt variant="small">Recent checks are off, so nothing you scan is stored. You can turn them on under About → Settings.</Txt>
        </Card>
      )}

      <Card tone="alt" style={{ flexDirection: 'row', gap: 12 }}>
        <IconBadge icon={Lightbulb} color={colors.amberBright} bg={colors.amberSoft} size={38} />
        <View style={{ flex: 1, gap: 2 }}>
          <Txt variant="overline" style={{ color: colors.amberBright }}>Hoshiyar tip</Txt>
          <Txt variant="small" style={{ color: colors.text }}>{tip}</Txt>
        </View>
      </Card>

      <Txt variant="caption" align="center">Model {version} · {s.aiCanBeWrong}</Txt>
    </Screen>
  );
}

function Tile({ icon, title, text, color, bg, onPress }: { icon: typeof Link2; title: string; text: string; color: string; bg: string; onPress: () => void }) {
  return (
    <Pressable accessibilityRole="button" accessibilityLabel={title} onPress={onPress} style={({ pressed }) => [styles.tile, pressed && { opacity: 0.8 }]}>
      <IconBadge icon={icon} color={color} bg={bg} size={40} />
      <Txt variant="title">{title}</Txt>
      <Txt variant="caption">{text}</Txt>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  top: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  iconBtn: { width: 42, height: 42, borderRadius: 12, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.surfaceAlt, borderWidth: 1, borderColor: colors.border },
  status: { flexDirection: 'row', gap: 12 },
  pulse: { width: 10, height: 10, borderRadius: 5, backgroundColor: colors.emeraldBright, marginTop: 6 },
  statusRow: { flexDirection: 'row', gap: 8, marginTop: 8, flexWrap: 'wrap' },
  pill: { flexDirection: 'row', alignItems: 'center', gap: 5, paddingHorizontal: 8, paddingVertical: 4, borderRadius: radius.pill, backgroundColor: 'rgba(16,185,129,0.12)' },
  primary: { flexDirection: 'row', alignItems: 'center', gap: 14, padding: 18, borderRadius: radius.xl },
  primaryIcon: { width: 56, height: 56, borderRadius: 18, backgroundColor: 'rgba(255,255,255,0.35)', alignItems: 'center', justifyContent: 'center' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  tile: { flexBasis: '47%', flexGrow: 1, gap: 6, padding: 14, borderRadius: radius.lg, backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border },
  historyRow: { flexDirection: 'row', alignItems: 'center', gap: 10, padding: 14 },
});
