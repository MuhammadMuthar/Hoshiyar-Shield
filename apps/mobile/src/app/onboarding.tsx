import { router } from 'expo-router';
import { Link2, Lock, Phone, ScanText, WifiOff } from 'lucide-react-native';
import { useEffect, useState } from 'react';
import { Animated, StyleSheet, View } from 'react-native';

import { Button } from '../components/Button';
import { Logo } from '../components/Logo';
import { Screen } from '../components/Screen';
import { Txt } from '../components/Txt';
import { IconBadge } from '../components/bits';
import { usePreferences } from '../features/preferences';
import { strings } from '../i18n';
import { colors } from '../theme';

const FEATURES = [
  { icon: ScanText, title: 'Analyse financial messages', text: 'Roman Urdu, Urdu and English, checked by a trained AI model.', color: colors.emerald, bg: colors.emeraldSoft },
  { icon: Link2, title: 'Spot suspicious links', text: 'Look-alike bank domains, hidden destinations and phishing tricks.', color: colors.teal, bg: colors.tealSoft },
  { icon: Phone, title: 'Check reported payment numbers', text: 'See reports about a number before you send money.', color: colors.amber, bg: colors.amberSoft },
  { icon: Lock, title: 'Private, on-device analysis', text: 'Messages are analysed on your phone and never uploaded.', color: colors.sky, bg: colors.skySoft },
];

export default function Onboarding() {
  const { update } = usePreferences();
  const s = strings();
  const fade = useState(() => FEATURES.map(() => new Animated.Value(0)))[0];

  useEffect(() => {
    Animated.stagger(110, fade.map((v) => Animated.timing(v, { toValue: 1, duration: 420, useNativeDriver: true }))).start();
  }, [fade]);

  const finish = () => {
    update({ onboarded: true });
    router.replace('/home');
  };

  return (
    <Screen footer={<Button label={s.getProtected} onPress={finish} size="lg" testID="get-protected" />}>
      <View style={styles.hero}>
        <View style={styles.logoRing}>
          <Logo size={76} />
        </View>
        <Txt variant="overline" style={{ color: colors.emeraldBright }}>Hoshiyar Shield</Txt>
        <Txt variant="display" align="center">{s.welcomeTitle}</Txt>
        <Txt variant="body" align="center" style={{ maxWidth: 330 }}>{s.welcomeBody}</Txt>
      </View>
      <View style={{ gap: 12 }}>
        {FEATURES.map((f, i) => (
          <Animated.View
            key={f.title}
            style={[styles.feature, { opacity: fade[i], transform: [{ translateY: fade[i].interpolate({ inputRange: [0, 1], outputRange: [14, 0] }) }] }]}
          >
            <IconBadge icon={f.icon} color={f.color} bg={f.bg} />
            <View style={{ flex: 1 }}>
              <Txt variant="title">{f.title}</Txt>
              <Txt variant="small">{f.text}</Txt>
            </View>
          </Animated.View>
        ))}
      </View>
      <View style={styles.note}>
        <WifiOff size={14} color={colors.textDim} />
        <Txt variant="caption" style={{ flex: 1 }}>
          No permissions needed. Hoshiyar never reads your SMS automatically: you choose what to check.
        </Txt>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  hero: { alignItems: 'center', gap: 10, paddingTop: 28, paddingBottom: 8 },
  logoRing: {
    width: 116, height: 116, borderRadius: 58, alignItems: 'center', justifyContent: 'center',
    backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, marginBottom: 6,
  },
  feature: { flexDirection: 'row', alignItems: 'center', gap: 14, backgroundColor: colors.surface, borderRadius: 18, padding: 14, borderWidth: 1, borderColor: colors.border },
  note: { flexDirection: 'row', gap: 8, alignItems: 'center', paddingHorizontal: 4 },
});
