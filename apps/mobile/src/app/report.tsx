import { router, useLocalSearchParams } from 'expo-router';
import { CheckCircle2, Flag, Lock, Square, SquareCheck } from 'lucide-react-native';
import { useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Screen } from '../components/Screen';
import { Txt } from '../components/Txt';
import { Chip, Field, Notice, SectionHeader, ToggleRow } from '../components/bits';
import { buildReport, checkRateLimit, MAX_DESCRIPTION, validateReport, type ReportErrors } from '../engine/reports';
import { CATEGORY_LABEL, type ScamCategory } from '../engine/reputation';
import { loadReports, saveReport } from '../features/reports';
import { getCurrentAnalysis } from '../features/session';
import { colors } from '../theme';

const CATEGORIES = Object.keys(CATEGORY_LABEL) as ScamCategory[];

export default function Report() {
  const params = useLocalSearchParams<{ target?: string; fromScan?: string }>();
  const fromScan = params.fromScan === '1' && !!getCurrentAnalysis();
  const [target, setTarget] = useState(typeof params.target === 'string' ? params.target : '');
  const [category, setCategory] = useState<ScamCategory | null>(null);
  const [description, setDescription] = useState('');
  const [includeMessage, setIncludeMessage] = useState(false);
  const [consent, setConsent] = useState(false);
  const [errors, setErrors] = useState<ReportErrors>({});
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const submit = async () => {
    const draft = { target, category, description, includeMessage, consent, messageText: fromScan ? getCurrentAnalysis()?.text : undefined };
    const e = validateReport(draft);
    if (Object.keys(e).length) {
      setErrors(e);
      return;
    }
    setSaving(true);
    const rate = checkRateLimit(await loadReports());
    if (rate) {
      setErrors({ rate });
      setSaving(false);
      return;
    }
    const ok = await saveReport(buildReport(draft));
    setSaving(false);
    if (!ok) {
      setErrors({ rate: 'Could not save on this phone (storage unavailable). Please try again.' });
      return;
    }
    setSaved(true);
  };

  if (saved) {
    return (
      <Screen title="Report saved" back footer={<Button label="Done" onPress={() => (router.canGoBack() ? router.back() : router.replace('/home'))} />}>
        <Card tone="success" style={{ alignItems: 'center', gap: 10, paddingVertical: 28 }}>
          <CheckCircle2 size={48} color={colors.emeraldBright} />
          <Txt variant="h2" align="center">Shukriya! Report saved.</Txt>
          <Txt variant="body" align="center" style={{ color: colors.text }}>
            It is saved on this phone only. It now appears when you check this number, and in your local statistics.
          </Txt>
        </Card>
        <Notice text="This MVP does not submit reports to any national service, bank or police. To make an official complaint, contact your bank's helpline or the cybercrime reporting channels of the authorities." />
      </Screen>
    );
  }

  return (
    <Screen
      title="Report a Scam"
      subtitle="Help others stay hoshiyar"
      back
      testID="report-screen"
      footer={<Button label="Save report" icon={Flag} onPress={submit} loading={saving} testID="save-report" />}
    >
      <Field
        testID="report-target"
        label="Phone number or link that was used"
        value={target}
        onChangeText={(t) => { setTarget(t); setErrors((e) => ({ ...e, target: undefined })); }}
        placeholder="0399-5550142 or suspicious-site.example"
        autoCapitalize="none"
        autoCorrect={false}
        error={errors.target}
      />

      <SectionHeader title="What kind of scam?" />
      <View style={styles.chips}>
        {CATEGORIES.map((c) => (
          <Chip key={c} label={CATEGORY_LABEL[c]} selected={category === c} onPress={() => { setCategory(c); setErrors((e) => ({ ...e, category: undefined })); }} />
        ))}
      </View>
      {errors.category ? <Txt variant="caption" style={{ color: colors.redBright }}>{errors.category}</Txt> : null}

      <Field
        label={`What happened? (optional, max ${MAX_DESCRIPTION} characters)`}
        value={description}
        onChangeText={setDescription}
        placeholder="e.g. Asked me to pay a 'verification fee' for a prize"
        multiline
        style={{ minHeight: 96, textAlignVertical: 'top', paddingTop: 12 }}
        maxLength={MAX_DESCRIPTION + 20}
        error={errors.description}
        hint="Please don't include your own CNIC, card or account numbers."
      />

      {fromScan ? (
        <Card>
          <ToggleRow
            title="Attach the analysed message text"
            text="Off by default. The text is stored only on this phone, inside this report."
            value={includeMessage}
            onChange={setIncludeMessage}
            testID="include-message"
          />
        </Card>
      ) : null}

      <Pressable
        accessibilityRole="checkbox"
        accessibilityState={{ checked: consent }}
        onPress={() => { setConsent((v) => !v); setErrors((e) => ({ ...e, consent: undefined })); }}
        style={styles.consent}
        testID="consent"
      >
        {consent ? <SquareCheck size={22} color={colors.emeraldBright} /> : <Square size={22} color={errors.consent ? colors.red : colors.textMuted} />}
        <Txt variant="small" style={{ flex: 1, color: colors.text }}>
          I confirm this report describes a message or request I actually received. I understand a report is an unverified claim, not proof that the owner of a number did anything wrong.
        </Txt>
      </Pressable>
      {errors.consent ? <Txt variant="caption" style={{ color: colors.redBright }}>{errors.consent}</Txt> : null}
      {errors.rate ? <Notice tone="warning" text={errors.rate} /> : null}

      <View style={styles.private}>
        <Lock size={14} color={colors.textDim} />
        <Txt variant="caption" style={{ flex: 1 }}>Reports stay on this phone (no account, no upload). Limit: 5 reports per hour.</Txt>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: -6 },
  consent: { flexDirection: 'row', gap: 10, alignItems: 'flex-start', paddingVertical: 4 },
  private: { flexDirection: 'row', gap: 8, alignItems: 'center' },
});
