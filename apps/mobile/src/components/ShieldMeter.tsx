import { useEffect, useState } from 'react';
import { Animated, Easing, StyleSheet, View } from 'react-native';
import Svg, { Circle, Path } from 'react-native-svg';

import type { RiskLevel } from '../engine/analyze';
import { colors, riskStyle } from '../theme';
import { RiskIcon } from './RiskBadge';

const AnimatedCircle = Animated.createAnimatedComponent(Circle);

/**
 * Animated shield + ring. The ring shows the ML score (0–1). The shield
 * colour and icon show the final fused risk level.
 */
export function ShieldMeter({ level, score, size = 168 }: { level: RiskLevel; score: number; size?: number }) {
  const s = riskStyle[level];
  const progress = useState(() => new Animated.Value(0))[0];
  const pop = useState(() => new Animated.Value(0.85))[0];
  const r = 70;
  const circ = 2 * Math.PI * r;

  useEffect(() => {
    progress.setValue(0);
    pop.setValue(0.85);
    Animated.parallel([
      Animated.timing(progress, { toValue: Math.max(0.02, Math.min(1, score)), duration: 900, easing: Easing.out(Easing.cubic), useNativeDriver: false }),
      Animated.spring(pop, { toValue: 1, useNativeDriver: true, speed: 9, bounciness: 9 }),
    ]).start();
  }, [score, level, progress, pop]);

  const offset = progress.interpolate({ inputRange: [0, 1], outputRange: [circ, 0] });
  const Icon = RiskIcon[level];
  return (
    <View style={{ width: size, height: size }} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
      <Svg width={size} height={size} viewBox="0 0 160 160">
        <Circle cx={80} cy={80} r={r} stroke={colors.surfaceHigh} strokeWidth={10} fill="none" />
        <AnimatedCircle
          cx={80} cy={80} r={r} stroke={s.color} strokeWidth={10} fill="none" strokeLinecap="round"
          strokeDasharray={`${circ} ${circ}`} strokeDashoffset={offset as unknown as number} rotation={-90} origin="80, 80"
        />
        <Path d="M80 34 L108 45 V73 C108 93 96 108 80 116 C64 108 52 93 52 73 V45 Z" fill={s.soft} stroke={s.color} strokeWidth={2.5} />
      </Svg>
      <Animated.View style={[StyleSheet.absoluteFill, styles.center, { transform: [{ scale: pop }] }]}>
        <Icon size={size * 0.2} color={s.bright} strokeWidth={2.4} />
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({ center: { alignItems: 'center', justifyContent: 'center', paddingTop: 4 } });
