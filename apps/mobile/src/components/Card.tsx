import { StyleSheet, View, type ViewProps } from 'react-native';

import { colors, radius } from '../theme';

interface Props extends ViewProps {
  tone?: 'default' | 'alt' | 'accent' | 'warning' | 'danger' | 'success';
  padded?: boolean;
}

const toneStyle = {
  default: { backgroundColor: colors.surface, borderColor: colors.border },
  alt: { backgroundColor: colors.surfaceAlt, borderColor: colors.border },
  accent: { backgroundColor: colors.tealSoft, borderColor: 'rgba(20,184,166,0.35)' },
  warning: { backgroundColor: colors.amberSoft, borderColor: 'rgba(245,158,11,0.4)' },
  danger: { backgroundColor: colors.redSoft, borderColor: 'rgba(239,68,68,0.4)' },
  success: { backgroundColor: colors.emeraldSoft, borderColor: 'rgba(16,185,129,0.38)' },
};

export function Card({ tone = 'default', padded = true, style, ...rest }: Props) {
  return <View style={[styles.card, toneStyle[tone], padded && styles.padded, style]} {...rest} />;
}

const styles = StyleSheet.create({
  card: { borderRadius: radius.lg, borderWidth: 1 },
  padded: { padding: 16 },
});
