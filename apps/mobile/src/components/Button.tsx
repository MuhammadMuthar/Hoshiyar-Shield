import * as Haptics from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';
import type { LucideIcon } from 'lucide-react-native';
import { useState } from 'react';
import { ActivityIndicator, Animated, Pressable, StyleSheet, View, type ViewStyle } from 'react-native';

import { colors, font, radius } from '../theme';
import { Txt } from './Txt';

interface Props {
  label: string;
  onPress: () => void;
  icon?: LucideIcon;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'lg' | 'md' | 'sm';
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
  accessibilityHint?: string;
  testID?: string;
}

export function Button({ label, onPress, icon: Icon, variant = 'primary', size = 'md', disabled, loading, style, accessibilityHint, testID }: Props) {
  const scale = useState(() => new Animated.Value(1))[0];
  const to = (v: number) => Animated.spring(scale, { toValue: v, useNativeDriver: true, speed: 40, bounciness: 6 }).start();
  const h = size === 'lg' ? 58 : size === 'md' ? 50 : 40;
  const fg = variant === 'primary' ? colors.bgDeep : variant === 'danger' ? colors.white : colors.text;
  const inner = (
    <View style={[styles.inner, { height: h, paddingHorizontal: size === 'sm' ? 14 : 20 }]}>
      {loading ? (
        <ActivityIndicator color={fg} />
      ) : (
        <>
          {Icon ? <Icon size={size === 'sm' ? 16 : 20} color={fg} strokeWidth={2.4} /> : null}
          <Txt style={{ fontFamily: font.bold, fontSize: size === 'lg' ? 17 : size === 'md' ? 15 : 13, color: fg }}>{label}</Txt>
        </>
      )}
    </View>
  );
  return (
    <Animated.View style={[{ transform: [{ scale }], opacity: disabled ? 0.45 : 1 }, style]}>
      <Pressable
        testID={testID}
        accessibilityRole="button"
        accessibilityLabel={label}
        accessibilityHint={accessibilityHint}
        accessibilityState={{ disabled: !!disabled, busy: !!loading }}
        disabled={disabled || loading}
        onPressIn={() => to(0.97)}
        onPressOut={() => to(1)}
        onPress={() => {
          Haptics.selectionAsync().catch(() => undefined);
          onPress();
        }}
        style={[styles.base, variant !== 'primary' && variantStyle[variant]]}
      >
        {variant === 'primary' ? (
          <LinearGradient colors={[colors.emeraldBright, colors.teal]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={styles.gradient}>
            {inner}
          </LinearGradient>
        ) : (
          inner
        )}
      </Pressable>
    </Animated.View>
  );
}

const variantStyle = {
  secondary: { backgroundColor: colors.surfaceAlt, borderColor: colors.borderStrong, borderWidth: 1 },
  ghost: { backgroundColor: 'transparent', borderColor: colors.border, borderWidth: 1 },
  danger: { backgroundColor: colors.red },
};

const styles = StyleSheet.create({
  base: { borderRadius: radius.md, overflow: 'hidden' },
  gradient: { borderRadius: radius.md },
  inner: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 10 },
});
