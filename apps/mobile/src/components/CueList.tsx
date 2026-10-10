import { AlertTriangle, CheckCircle2, Info } from 'lucide-react-native';
import { StyleSheet, View } from 'react-native';

import type { Indicator } from '../engine/indicators';
import { colors } from '../theme';
import { Txt } from './Txt';

const SEVERITY_LABEL = { high: 'Strong warning', medium: 'Warning', low: 'Note' } as const;

export function CueList({ indicators }: { indicators: Indicator[] }) {
  return (
    <View style={{ gap: 10 }}>
      {indicators.map((ind) => {
        const protective = ind.kind === 'protective';
        const color = protective ? colors.emerald : ind.severity === 'high' ? colors.red : ind.severity === 'medium' ? colors.amber : colors.sky;
        const Icon = protective ? CheckCircle2 : ind.severity === 'low' ? Info : AlertTriangle;
        return (
          <View key={ind.id} style={styles.row} accessible accessibilityLabel={`${protective ? 'Reassuring' : SEVERITY_LABEL[ind.severity]}: ${ind.label}. ${ind.explanation}`}>
            <View style={[styles.bar, { backgroundColor: color }]} />
            <Icon size={18} color={color} style={{ marginTop: 2 }} />
            <View style={{ flex: 1, gap: 2 }}>
              <Txt variant="bodyStrong">{ind.label}</Txt>
              <Txt variant="small">{ind.explanation}</Txt>
              <Txt variant="caption" style={{ color }}>{protective ? 'Reassuring sign' : SEVERITY_LABEL[ind.severity]}</Txt>
            </View>
          </View>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: 10, backgroundColor: colors.surfaceAlt, borderRadius: 14, padding: 12, overflow: 'hidden' },
  bar: { position: 'absolute', left: 0, top: 0, bottom: 0, width: 3 },
});
