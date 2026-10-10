/** Small shared building blocks. */
import type { LucideIcon } from 'lucide-react-native';
import { Info } from 'lucide-react-native';
import type { ReactNode } from 'react';
import { Pressable, StyleSheet, Switch, TextInput, View, type TextInputProps } from 'react-native';

import { colors, font, radius } from '../theme';
import { Button } from './Button';
import { Txt } from './Txt';

export function IconBadge({ icon: Icon, color = colors.emerald, bg = colors.emeraldSoft, size = 44 }: { icon: LucideIcon; color?: string; bg?: string; size?: number }) {
  return (
    <View style={{ width: size, height: size, borderRadius: size * 0.32, backgroundColor: bg, alignItems: 'center', justifyContent: 'center' }}>
      <Icon size={size * 0.5} color={color} strokeWidth={2.2} />
    </View>
  );
}

export function SectionHeader({ title, action }: { title: string; action?: ReactNode }) {
  return (
    <View style={styles.sectionHeader}>
      <Txt variant="overline">{title}</Txt>
      {action}
    </View>
  );
}

export function Notice({ text, icon: Icon = Info, tone = 'info' }: { text: string; icon?: LucideIcon; tone?: 'info' | 'warning' | 'success' }) {
  const c = tone === 'warning' ? colors.amber : tone === 'success' ? colors.emerald : colors.sky;
  const bg = tone === 'warning' ? colors.amberSoft : tone === 'success' ? colors.emeraldSoft : colors.skySoft;
  return (
    <View style={[styles.notice, { backgroundColor: bg, borderColor: c + '55' }]}>
      <Icon size={16} color={c} style={{ marginTop: 2 }} />
      <Txt variant="small" style={{ flex: 1, color: colors.text }}>{text}</Txt>
    </View>
  );
}

export function EmptyState({ icon: Icon, title, text, actionLabel, onAction }: { icon: LucideIcon; title: string; text: string; actionLabel?: string; onAction?: () => void }) {
  return (
    <View style={styles.empty}>
      <IconBadge icon={Icon} color={colors.textMuted} bg={colors.surfaceAlt} size={56} />
      <Txt variant="title" align="center">{title}</Txt>
      <Txt variant="small" align="center">{text}</Txt>
      {actionLabel && onAction ? <Button label={actionLabel} onPress={onAction} variant="secondary" size="sm" /> : null}
    </View>
  );
}

export function Field({ label, error, hint, style, ...rest }: TextInputProps & { label?: string; error?: string; hint?: string }) {
  return (
    <View style={{ gap: 6 }}>
      {label ? <Txt variant="caption" style={{ color: colors.textMuted }}>{label}</Txt> : null}
      <TextInput
        placeholderTextColor={colors.textDim}
        selectionColor={colors.emerald}
        accessibilityLabel={label}
        style={[styles.input, error ? { borderColor: colors.red } : null, style]}
        {...rest}
      />
      {error ? <Txt variant="caption" style={{ color: colors.redBright }}>{error}</Txt> : hint ? <Txt variant="caption">{hint}</Txt> : null}
    </View>
  );
}

export function Chip({ label, selected, onPress, icon: Icon }: { label: string; selected?: boolean; onPress: () => void; icon?: LucideIcon }) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ selected: !!selected }}
      onPress={onPress}
      style={[styles.chip, selected && { backgroundColor: colors.emeraldSoft, borderColor: colors.emerald }]}
    >
      {Icon ? <Icon size={14} color={selected ? colors.emeraldBright : colors.textMuted} /> : null}
      <Txt style={{ fontFamily: font.semibold, fontSize: 13, color: selected ? colors.emeraldBright : colors.textMuted }}>{label}</Txt>
    </Pressable>
  );
}

export function ToggleRow({ title, text, value, onChange, testID }: { title: string; text: string; value: boolean; onChange: (v: boolean) => void; testID?: string }) {
  return (
    <View style={styles.toggle}>
      <View style={{ flex: 1, gap: 2 }}>
        <Txt variant="title">{title}</Txt>
        <Txt variant="small">{text}</Txt>
      </View>
      <Switch
        testID={testID}
        accessibilityLabel={title}
        value={value}
        onValueChange={onChange}
        trackColor={{ false: colors.surfaceHigh, true: colors.emerald }}
        thumbColor={colors.white}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  sectionHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: 8 },
  notice: { flexDirection: 'row', gap: 10, padding: 12, borderRadius: radius.md, borderWidth: 1 },
  empty: { alignItems: 'center', gap: 8, paddingVertical: 28, paddingHorizontal: 16 },
  input: {
    minHeight: 52, borderRadius: radius.md, borderWidth: 1, borderColor: colors.borderStrong, backgroundColor: colors.surface,
    color: colors.text, paddingHorizontal: 14, fontFamily: font.medium, fontSize: 16,
  },
  chip: {
    flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 8,
    borderRadius: radius.pill, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.surface,
  },
  toggle: { flexDirection: 'row', alignItems: 'center', gap: 12, paddingVertical: 6 },
});
