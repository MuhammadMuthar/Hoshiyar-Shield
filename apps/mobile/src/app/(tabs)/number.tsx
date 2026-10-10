import { useFocusEffect, router } from 'expo-router';
import { CalendarDays, Database, Flag, Phone, Search, ShieldAlert, Smartphone } from 'lucide-react-native';
import { useMemo, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { Screen } from '../../components/Screen';
import { Txt } from '../../components/Txt';
import { Chip, EmptyState, Field, IconBadge, Notice, SectionHeader } from '../../components/bits';
import { normalizePkMobile, type PhoneParseOk } from '../../engine/phone';
import { CATEGORY_LABEL, lookupNumber, type ReputationSummary } from '../../engine/reputation';
import { addHistory } from '../../features/history';
import { usePreferences } from '../../features/preferences';
import { toReputationRecords, useReports } from '../../features/reports';
import { colors, font } from '../../theme';

const DEMO_NUMBERS = ['0399-5550142', '0399-5550160', '0399-5550193', '0399-5550777'];

export default function NumberCheck() {
  const prefs = usePreferences();
  const { reports, refresh } = useReports();
  useFocusEffect(refresh);
  const local = useMemo(() => toReputationRecords(reports), [reports]);
  const [input, setInput] = useState('');
  const [parsed, setParsed] = useState<PhoneParseOk | null>(null);
  const [summary, setSummary] = useState<ReputationSummary | null>(null);
  const [error, setError] = useState<string | undefined>();

  const check = (value = input) => {
    const p = normalizePkMobile(value);
    if (!p.ok) {
      setError(p.message);
      setParsed(null);
      setSummary(null);
      return;
    }
    setError(undefined);
    setParsed(p);
    const s = lookupNumber(p.e164, local, prefs.demoMode);
    setSummary(s);
    void addHistory({ kind: 'number', level: s.level === 'reported' ? 'REPORTED' : 'NONE', preview: p.display }, prefs.saveHistory);
  };

  return (
    <Screen title="Check a Number" subtitle="Before you send money to a wallet or mobile number" testID="number-screen">
      <Field
        testID="number-input"
        label="Pakistani mobile / wallet number"
        value={input}
        onChangeText={(t) => { setInput(t); setError(undefined); }}
        placeholder="03xx-xxxxxxx or +92 3xx xxxxxxx"
        keyboardType="phone-pad"
        returnKeyType="search"
        onSubmitEditing={() => check()}
        error={error}
      />
      <Button label="Check number" icon={Search} onPress={() => check()} disabled={!input.trim()} testID="check-number" />
      {prefs.demoMode ? (
        <View style={styles.chips}>
          {DEMO_NUMBERS.map((n) => <Chip key={n} label={n} icon={Phone} onPress={() => { setInput(n); check(n); }} />)}
        </View>
      ) : null}

      {parsed && summary ? (
        <View style={{ gap: 14 }} testID="number-result">
          <Card style={{ gap: 10, ...(summary.level === 'reported' ? { borderColor: colors.amber + '99', backgroundColor: colors.amberSoft } : {}) }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
              <IconBadge icon={summary.level === 'reported' ? ShieldAlert : Smartphone} color={summary.level === 'reported' ? colors.amberBright : colors.textMuted} bg={summary.level === 'reported' ? colors.amberSoft : colors.surfaceAlt} />
              <View style={{ flex: 1 }}>
                <Txt style={{ fontFamily: font.bold, fontSize: 22, color: colors.text }} selectable>{parsed.display}</Txt>
                <Txt variant="caption">{parsed.e164} · {parsed.prefixNetwork} (numbers can be ported)</Txt>
              </View>
            </View>
            <Txt variant="title" testID="number-headline">{summary.headline}</Txt>
          </Card>

          {summary.total ? (
            <>
              <SectionHeader title={`Reports (${summary.total})`} />
              <Card style={{ gap: 10 }}>
                {summary.categories.map((c) => (
                  <View key={c.category} style={styles.row}>
                    <Txt variant="bodyStrong" style={{ flex: 1 }}>{c.label}</Txt>
                    <Txt variant="bodyStrong" style={{ color: colors.amberBright }}>{c.count}</Txt>
                  </View>
                ))}
                <View style={styles.row}>
                  <CalendarDays size={14} color={colors.textDim} />
                  <Txt variant="caption" style={{ flex: 1 }}>Most recent report: {summary.lastReported}{summary.firstReported !== summary.lastReported ? ` (first: ${summary.firstReported})` : ''}</Txt>
                </View>
                <View style={styles.row}>
                  <Database size={14} color={colors.textDim} />
                  <Txt variant="caption" style={{ flex: 1 }}>
                    Sources: {summary.demoCount ? `${summary.demoCount} synthetic demo record(s)` : ''}{summary.demoCount && summary.localCount ? ' + ' : ''}{summary.localCount ? `${summary.localCount} saved on this phone` : ''}
                  </Txt>
                </View>
                {summary.records.filter((r) => r.note).slice(0, 3).map((r, i) => (
                  <Txt key={i} variant="small">• “{r.note}” ({CATEGORY_LABEL[r.category]}, {r.date}{r.source === 'demo' ? ', DEMO' : ', yours'})</Txt>
                ))}
              </Card>
            </>
          ) : null}

          <Card tone="alt" style={{ gap: 8 }}>
            {summary.caveats.map((c) => <Txt key={c} variant="small" style={{ color: colors.text }}>• {c}</Txt>)}
          </Card>
          <Button label="Report this number" icon={Flag} variant="secondary" onPress={() => router.push({ pathname: '/report', params: { target: parsed.display } })} />
          <Notice text="Hoshiyar does not block or make payments. It only shows reports. Check the account holder's name in your banking app before you confirm any transfer." />
        </View>
      ) : (
        !error && <EmptyState icon={Phone} title="Check before you pay" text="Enter the number you were asked to send money to. We'll show any reports, and remind you that an unreported number is not automatically safe." />
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 8 },
});
