import { ShieldAlert, ShieldCheck, ShieldX } from 'lucide-react-native';
import { StyleSheet, View } from 'react-native';

import type { RiskLevel } from '../engine/analyze';
import { font, radius, riskStyle } from '../theme';
import { Txt } from './Txt';

export const RiskIcon = { HIGH: ShieldX, SUSPICIOUS: ShieldAlert, LOW: ShieldCheck } as const;

/** Risk is always shown with an icon AND a word, never colour alone. */
export function RiskBadge({ level, compact }: { level: RiskLevel; compact?: boolean }) {
  const s = riskStyle[level];
  const Icon = RiskIcon[level];
  return (
    <View style={[styles.badge, { backgroundColor: s.soft, borderColor: s.color }]} accessibilityLabel={`Risk: ${s.label}`}>
      <Icon size={compact ? 13 : 15} color={s.bright} strokeWidth={2.5} />
      <Txt style={{ fontFamily: font.bold, fontSize: compact ? 11 : 12, color: s.bright, letterSpacing: 0.6 }}>
        {compact ? s.short : s.label.toUpperCase()}
      </Txt>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    flexDirection: 'row', alignItems: 'center', gap: 6, alignSelf: 'flex-start',
    paddingHorizontal: 10, paddingVertical: 5, borderRadius: radius.pill, borderWidth: 1,
  },
});
