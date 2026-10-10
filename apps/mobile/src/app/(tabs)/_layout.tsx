import { Tabs } from 'expo-router/tabs';
import { Link2, Phone, Radar, ScanText, ShieldCheck } from 'lucide-react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { colors, font } from '../../theme';

export default function TabsLayout() {
  const insets = useSafeAreaInsets();
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.emeraldBright,
        tabBarInactiveTintColor: colors.textDim,
        tabBarStyle: {
          backgroundColor: colors.bgDeep,
          borderTopColor: colors.border,
          height: 70 + insets.bottom,
          paddingTop: 8,
          paddingBottom: insets.bottom + 10,
        },
        tabBarLabelStyle: { fontFamily: font.semibold, fontSize: 11 },
        sceneStyle: { backgroundColor: colors.bg },
      }}
    >
      <Tabs.Screen name="home" options={{ title: 'Home', tabBarIcon: ({ color, size }) => <ShieldCheck color={color} size={size} /> }} />
      <Tabs.Screen name="scan" options={{ title: 'Scan', tabBarIcon: ({ color, size }) => <ScanText color={color} size={size} /> }} />
      <Tabs.Screen name="link" options={{ title: 'Link', tabBarIcon: ({ color, size }) => <Link2 color={color} size={size} /> }} />
      <Tabs.Screen name="number" options={{ title: 'Number', tabBarIcon: ({ color, size }) => <Phone color={color} size={size} /> }} />
      <Tabs.Screen name="intel" options={{ title: 'Intel', tabBarIcon: ({ color, size }) => <Radar color={color} size={size} /> }} />
    </Tabs>
  );
}
