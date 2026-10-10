import Svg, { Defs, LinearGradient, Path, Stop } from 'react-native-svg';

import { colors } from '../theme';

/** Hoshiyar Shield mark: a shield with an eye-like "H" check. */
export function Logo({ size = 40 }: { size?: number }) {
  return (
    <Svg width={size} height={size} viewBox="0 0 64 64" accessibilityLabel="Hoshiyar Shield logo">
      <Defs>
        <LinearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
          <Stop offset="0" stopColor={colors.emeraldBright} />
          <Stop offset="1" stopColor={colors.teal} />
        </LinearGradient>
      </Defs>
      <Path
        d="M32 4 L54 12 V30 C54 44 44.5 54.5 32 60 C19.5 54.5 10 44 10 30 V12 Z"
        fill="url(#lg)"
      />
      <Path
        d="M32 9.5 L49 15.8 V30 C49 41.2 41.6 49.6 32 54.2 C22.4 49.6 15 41.2 15 30 V15.8 Z"
        fill={colors.bg}
        opacity={0.92}
      />
      <Path d="M24 22 V40 M40 22 V40 M24 31 H40" stroke="url(#lg)" strokeWidth={5} strokeLinecap="round" fill="none" />
    </Svg>
  );
}
