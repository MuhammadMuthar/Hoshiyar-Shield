import { StyleSheet, Text, type TextProps, type TextStyle } from 'react-native';

import { colors, font, isRtl } from '../theme';

type Variant = 'display' | 'h1' | 'h2' | 'title' | 'body' | 'bodyStrong' | 'small' | 'caption' | 'overline' | 'mono';

interface Props extends TextProps {
  variant?: Variant;
  color?: string;
  align?: TextStyle['textAlign'];
  /** Detect Urdu script and render right-to-left. */
  autoDirection?: boolean;
}

export function Txt({ variant = 'body', color, align, autoDirection, style, children, ...rest }: Props) {
  const dir: TextStyle | undefined =
    autoDirection && typeof children === 'string' && isRtl(children)
      ? { writingDirection: 'rtl', textAlign: 'right', fontFamily: undefined, lineHeight: 30 }
      : undefined;
  return (
    <Text
      maxFontSizeMultiplier={1.6}
      style={[styles[variant], color ? { color } : null, align ? { textAlign: align } : null, style, dir]}
      {...rest}
    >
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  display: { fontFamily: font.extrabold, fontSize: 32, lineHeight: 38, color: colors.text, letterSpacing: -0.6 },
  h1: { fontFamily: font.bold, fontSize: 26, lineHeight: 32, color: colors.text, letterSpacing: -0.4 },
  h2: { fontFamily: font.bold, fontSize: 20, lineHeight: 26, color: colors.text, letterSpacing: -0.2 },
  title: { fontFamily: font.semibold, fontSize: 16, lineHeight: 22, color: colors.text },
  body: { fontFamily: font.regular, fontSize: 15, lineHeight: 22, color: colors.textMuted },
  bodyStrong: { fontFamily: font.medium, fontSize: 15, lineHeight: 22, color: colors.text },
  small: { fontFamily: font.regular, fontSize: 13, lineHeight: 19, color: colors.textMuted },
  caption: { fontFamily: font.medium, fontSize: 12, lineHeight: 16, color: colors.textDim },
  overline: { fontFamily: font.bold, fontSize: 11, lineHeight: 14, color: colors.textDim, letterSpacing: 1.2, textTransform: 'uppercase' },
  mono: { fontFamily: font.medium, fontSize: 13, lineHeight: 18, color: colors.textMuted, letterSpacing: 0.2 },
});
