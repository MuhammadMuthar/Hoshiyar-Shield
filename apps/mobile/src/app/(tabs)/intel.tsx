import { useFocusEffect } from 'expo-router';
import { FlaskConical, Layers, MessageSquareWarning, Radar, Smartphone } from 'lucide-react-native';
import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import campaignsJson from '../../../assets/model/campaigns.json';
import { Card } from '../../components/Card';
import { Screen } from '../../components/Screen';
import { Txt } from '../../components/Txt';
import { IconBadge, Notice, SectionHeader } from '../../components/bits';
import { maskNumber } from '../../engine/phone';
import { CATEGORY_LABEL } from '../../engine/reputation';
import { useReports } from '../../features/reports';
import { colors, font, radius } from '../../theme';

interface Campaign {
  campaign_id: string;
  report_count: number;
  dominant_category: string;
  dominant_category_label: string;
  category_share: number;
  representative_pattern: string;
  first_seen: string;
  last_seen: string;
  top_terms: string[];
  weekly_reports: number[];
  contact_methods: Record<string, number>;
}
interface CampaignDoc {
  disclaimer: string;
  method: string;
  window: { start: string; end: string };
  total_reports: number;
  clustered_reports: number;
  reports_by_category: Record<string, { label: string; count: number }>;
  weekly_reports: number[];
  contact_methods: Record<string, number>;
  top_phrases: { phrase: string; count: number }[];
  evaluation: { mean_family_purity: number; clusters_found: number };
  campaigns: Campaign[];
}
const DOC = campaignsJson as unknown as CampaignDoc;
const BAR = colors.teal; // single hue: magnitude only. Status colours stay reserved for risk.

export default function Intel() {
  const { reports, refresh } = useReports();
  useFocusEffect(refresh);
  const [week, setWeek] = useState<number | null>(null);
  const cats = Object.entries(DOC.reports_by_category);
  const maxCat = Math.max(...cats.map(([, v]) => v.count));
  const maxWeek = Math.max(...DOC.weekly_reports);
  const weekStart = (i: number) => {
    const d = new Date(DOC.window.start + 'T00:00:00Z');
    d.setUTCDate(d.getUTCDate() + i * 7);
    return d.toISOString().slice(5, 10);
  };
  const localByCat = useMemo(() => {
    const m = new Map<string, number>();
    reports.forEach((r) => m.set(r.category, (m.get(r.category) ?? 0) + 1));
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [reports]);

  return (
    <Screen title="Scam Intelligence" subtitle="How consented reports could reveal scam campaigns" testID="intel-screen">
      <Notice tone="warning" icon={FlaskConical} text={DOC.disclaimer} />

      <View style={styles.tiles}>
        <Stat label="Simulated reports" value={DOC.total_reports} />
        <Stat label="Campaigns found" value={DOC.campaigns.length} />
        <Stat label="Grouped" value={`${Math.round((DOC.clustered_reports / DOC.total_reports) * 100)}%`} />
      </View>

      <SectionHeader title="Reports by scam type" />
      <Card style={{ gap: 10 }} accessibilityLabel={'Reports by scam type: ' + cats.map(([, v]) => `${v.label} ${v.count}`).join(', ')}>
        {cats.map(([k, v]) => (
          <View key={k} style={{ gap: 4 }}>
            <View style={styles.rowBetween}>
              <Txt variant="small" style={{ color: colors.text }}>{v.label}</Txt>
              <Txt variant="small" style={{ color: colors.text, fontFamily: font.semibold }}>{v.count}</Txt>
            </View>
            <View style={styles.hTrack}>
              <View style={[styles.hBar, { width: `${(v.count / maxCat) * 100}%` }]} />
            </View>
          </View>
        ))}
      </Card>

      <SectionHeader title="Reports per week" />
      <Card style={{ gap: 10 }}>
        <Txt variant="small" style={{ color: colors.text }}>
          {week === null ? 'Tap a bar to see its value.' : `Week of ${weekStart(week)}: ${DOC.weekly_reports[week]} reports`}
        </Txt>
        <View style={styles.columns} accessibilityLabel={'Weekly reports: ' + DOC.weekly_reports.map((n, i) => `week of ${weekStart(i)} ${n}`).join(', ')}>
          {DOC.weekly_reports.map((n, i) => (
            <Pressable key={i} style={styles.colHit} onPress={() => setWeek(i === week ? null : i)} accessibilityRole="button" accessibilityLabel={`Week of ${weekStart(i)}: ${n} reports`}>
              <View style={[styles.col, { height: `${Math.max(4, (n / maxWeek) * 100)}%`, opacity: week === null || week === i ? 1 : 0.45 }]} />
            </Pressable>
          ))}
        </View>
        <View style={styles.rowBetween}>
          <Txt variant="caption">{weekStart(0)}</Txt>
          <Txt variant="caption">{weekStart(DOC.weekly_reports.length - 1)}</Txt>
        </View>
      </Card>

      <SectionHeader title="Detected campaigns" action={<Txt variant="caption">{DOC.campaigns.length}</Txt>} />
      <Txt variant="small" style={{ marginTop: -8 }}>
        Differently worded reports grouped by AI similarity. Analysts can review a campaign instead of hundreds of separate complaints.
      </Txt>
      {DOC.campaigns.map((c) => (
        <Card key={c.campaign_id} style={{ gap: 10 }}>
          <View style={styles.rowBetween}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10, flex: 1 }}>
              <IconBadge icon={Layers} color={colors.teal} bg={colors.tealSoft} size={36} />
              <View style={{ flex: 1 }}>
                <Txt variant="title">{c.campaign_id} · {c.dominant_category_label}</Txt>
                <Txt variant="caption">{c.first_seen} → {c.last_seen}</Txt>
              </View>
            </View>
            <View style={styles.countPill}>
              <Txt style={{ fontFamily: font.bold, fontSize: 13, color: colors.text }}>{c.report_count}</Txt>
              <Txt variant="caption">reports</Txt>
            </View>
          </View>
          <View style={styles.pattern}>
            <Txt variant="small" autoDirection style={{ color: colors.text }} numberOfLines={3}>{c.representative_pattern}</Txt>
          </View>
          <View style={styles.terms}>
            {c.top_terms.slice(0, 4).map((t) => (
              <View key={t} style={styles.term}><Txt variant="caption" style={{ color: colors.textMuted }}>{t}</Txt></View>
            ))}
          </View>
        </Card>
      ))}

      <SectionHeader title="Most common phrases" />
      <Card style={{ gap: 8 }}>
        {DOC.top_phrases.slice(0, 6).map((p) => (
          <View key={p.phrase} style={styles.rowBetween}>
            <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center', flex: 1 }}>
              <MessageSquareWarning size={14} color={colors.textDim} />
              <Txt variant="small" style={{ color: colors.text }} autoDirection>“{p.phrase}”</Txt>
            </View>
            <Txt variant="caption">{p.count}×</Txt>
          </View>
        ))}
      </Card>

      <SectionHeader title="Your reports on this phone" />
      <Card style={{ gap: 8 }}>
        {reports.length ? (
          <>
            <Txt variant="small" style={{ color: colors.text }}>{reports.length} saved report(s). These are real but unverified, and stay on this phone.</Txt>
            {localByCat.map(([k, n]) => (
              <View key={k} style={styles.rowBetween}>
                <Txt variant="small">{CATEGORY_LABEL[k as keyof typeof CATEGORY_LABEL] ?? k}</Txt>
                <Txt variant="small" style={{ color: colors.text }}>{n}</Txt>
              </View>
            ))}
            {reports.filter((r) => r.targetType === 'phone').slice(0, 3).map((r) => (
              <View key={r.id} style={{ flexDirection: 'row', gap: 6, alignItems: 'center' }}>
                <Smartphone size={13} color={colors.textDim} />
                <Txt variant="caption">{maskNumber(r.target)} · {r.createdAt.slice(0, 10)}</Txt>
              </View>
            ))}
          </>
        ) : (
          <Txt variant="small">You haven’t saved any reports yet. Reports you save appear here and in number checks.</Txt>
        )}
      </Card>

      <Card tone="alt" style={{ flexDirection: 'row', gap: 12 }}>
        <IconBadge icon={Radar} color={colors.sky} bg={colors.skySoft} size={36} />
        <View style={{ flex: 1, gap: 4 }}>
          <Txt variant="title">How grouping works</Txt>
          <Txt variant="small">{DOC.method}.</Txt>
          <Txt variant="small">
            On this synthetic set, grouped campaigns match the message family that generated them {Math.round(DOC.evaluation.mean_family_purity * 100)}% of the time. Similar wording does not prove the same people are behind messages.
          </Txt>
        </View>
      </Card>
    </Screen>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <View style={styles.stat}>
      <Txt style={{ fontFamily: font.extrabold, fontSize: 24, color: colors.text }}>{value}</Txt>
      <Txt variant="caption">{label}</Txt>
    </View>
  );
}

const styles = StyleSheet.create({
  tiles: { flexDirection: 'row', gap: 10 },
  stat: { flex: 1, padding: 12, borderRadius: radius.md, backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, gap: 2 },
  rowBetween: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 8 },
  hTrack: { height: 8, borderRadius: 4, backgroundColor: colors.surfaceHigh },
  hBar: { height: 8, borderRadius: 4, backgroundColor: BAR },
  columns: { flexDirection: 'row', alignItems: 'flex-end', height: 110, gap: 6 },
  colHit: { flex: 1, height: '100%', justifyContent: 'flex-end' },
  col: { backgroundColor: BAR, borderTopLeftRadius: 4, borderTopRightRadius: 4 },
  countPill: { alignItems: 'center', paddingHorizontal: 10, paddingVertical: 4, borderRadius: radius.sm, backgroundColor: colors.surfaceAlt },
  pattern: { padding: 10, borderRadius: radius.sm, backgroundColor: colors.surfaceAlt, borderLeftWidth: 3, borderLeftColor: colors.teal },
  terms: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  term: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: radius.pill, borderWidth: 1, borderColor: colors.border },
});
