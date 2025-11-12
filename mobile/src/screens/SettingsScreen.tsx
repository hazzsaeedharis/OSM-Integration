/**
 * Settings Screen - Language selection and app info
 */

import React, {useState, useEffect} from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  ScrollView,
  Switch,
} from 'react-native';
import {useTranslation} from 'react-i18next';
import ApiService, {Statistics} from '../services/api';
import colors from '../theme/colors';

export default function SettingsScreen() {
  const {t, i18n} = useTranslation();
  const [stats, setStats] = useState<Statistics | null>(null);
  const [isDeutsch, setIsDeutsch] = useState(i18n.language === 'de');

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      const data = await ApiService.getStatistics();
      setStats(data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  const toggleLanguage = (value: boolean) => {
    setIsDeutsch(value);
    i18n.changeLanguage(value ? 'de' : 'en');
  };

  return (
    <ScrollView style={styles.container}>
      {/* Language Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🌐 {t('language')}</Text>
        
        <View style={styles.languageCard}>
          <Text style={styles.languageLabel}>
            {isDeutsch ? '🇩🇪 Deutsch' : '🇬🇧 English'}
          </Text>
          <Switch
            value={isDeutsch}
            onValueChange={toggleLanguage}
            trackColor={{false: colors.border, true: colors.primary}}
            thumbColor={colors.background}
          />
        </View>
      </View>

      {/* Statistics Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📊 {t('businesses')}</Text>
        
        {stats && (
          <>
            <View style={styles.statCard}>
              <Text style={styles.statValue}>
                {stats.total_businesses.toLocaleString()}
              </Text>
              <Text style={styles.statLabel}>{t('businesses')}</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statValue}>
                {stats.geocoded_businesses.toLocaleString()}
              </Text>
              <Text style={styles.statLabel}>{t('with_coordinates')}</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statValue}>
                {stats.unique_cities.toLocaleString()}
              </Text>
              <Text style={styles.statLabel}>Cities / Districts</Text>
            </View>
          </>
        )}
      </View>

      {/* About Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>ℹ️ {t('about')}</Text>
        
        <View style={styles.aboutCard}>
          <Text style={styles.aboutTitle}>Berlin Business Finder</Text>
          <Text style={styles.aboutText}>{t('version')}</Text>
          <Text style={styles.aboutText}>{t('data_source')}</Text>
          <Text style={styles.aboutText}>{t('map_data')}</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.backgroundLight,
  },
  section: {
    padding: 15,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: 15,
  },
  languageCard: {
    backgroundColor: colors.background,
    padding: 20,
    borderRadius: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  languageLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  statCard: {
    backgroundColor: colors.background,
    padding: 20,
    borderRadius: 10,
    marginBottom: 10,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: colors.primary,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  statLabel: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 5,
  },
  aboutCard: {
    backgroundColor: colors.background,
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  aboutTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: 10,
  },
  aboutText: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 5,
  },
  searchSection: {
    padding: 15,
    backgroundColor: colors.background,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  searchInput: {
    height: 45,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    paddingHorizontal: 15,
    backgroundColor: colors.background,
    fontSize: 16,
  },
  filtersSection: {
    padding: 15,
    backgroundColor: colors.background,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  pickerContainer: {
    marginBottom: 15,
  },
  filterLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 5,
  },
  picker: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
  },
  actionButtons: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: colors.background,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  button: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  listContent: {
    padding: 15,
  },
  businessCard: {
    backgroundColor: colors.background,
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: colors.primary,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  businessName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: 8,
  },
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 8,
  },
  categoryBadge: {
    backgroundColor: colors.primary,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 6,
    marginBottom: 4,
  },
  categoryText: {
    color: colors.textPrimary,
    fontSize: 11,
    fontWeight: '600',
  },
  businessLocation: {
    fontSize: 13,
    color: colors.textSecondary,
  },
  loadingCenter: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 60,
  },
  emptySubtext: {
    fontSize: 16,
    color: colors.textSecondary,
  },
});

