import { Redirect } from 'expo-router';
import { View } from 'react-native';

import { usePreferences } from '../features/preferences';
import { colors } from '../theme';

/** Entry: first-time users see onboarding, everyone else goes to Home. */
export default function Index() {
  const { loaded, onboarded } = usePreferences();
  if (!loaded) return <View style={{ flex: 1, backgroundColor: colors.bg }} />;
  return <Redirect href={onboarded ? '/home' : '/onboarding'} />;
}
