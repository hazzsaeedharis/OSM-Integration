/**
 * Business Detail Screen - Full business information
 */

import React, {useState, useEffect} from 'react';
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Linking,
} from 'react-native';
import {useRoute, RouteProp} from '@react-navigation/native';
import {useTranslation} from 'react-i18next';
import ApiService, {Business} from '../services/api';
import colors from '../theme/colors';
import {RootStackParamList} from '../navigation/AppNavigator';

type BusinessDetailRouteProp = RouteProp<RootStackParamList, 'BusinessDetail'>;

export default function BusinessDetailScreen() {
  const {t} = useTranslation();
  const route = useRoute<BusinessDetailRouteProp>();
  const [business, setBusiness] = useState<Business | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBusiness();
  }, []);

  const loadBusiness = async () => {
    try {
      const data = await ApiService.getBusiness(route.params.businessId);
      setBusiness(data);
    } catch (error) {
      console.error('Error loading business:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetDirections = () => {
    if (business?.lat && business?.lon) {
      const url = `https://www.google.com/maps/search/?api=1&query=${business.lat},${business.lon}`;
      Linking.openURL(url);
    }
  };

  const handleSearchGoogle = () => {
    if (business) {
      const query = encodeURIComponent(
        `${business.name} ${business.postal_code} ${business.city}`,
      );
      const url = `https://www.google.com/search?q=${query}`;
      Linking.openURL(url);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>{t('loading')}</Text>
      </View>
    );
  }

  if (!business) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{t('error_loading')}</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Business Name */}
      <View style={styles.header}>
        <Text style={styles.businessName}>{business.name}</Text>
      </View>

      {/* Categories */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>{t('categories')}</Text>
        <View style={styles.categoriesContainer}>
          {business.categories.map((cat, index) => (
            <View key={index} style={styles.categoryBadge}>
              <Text style={styles.categoryText}>{cat}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* Location */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📍 {t('location')}</Text>
        <View style={styles.infoCard}>
          <Text style={styles.infoText}>
            {business.postal_code} {business.city}
          </Text>
        </View>
      </View>

      {/* Coordinates */}
      {business.lat && business.lon && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🗺️ {t('coordinates')}</Text>
          <View style={styles.infoCard}>
            <Text style={styles.infoText}>
              {business.lat.toFixed(6)}, {business.lon.toFixed(6)}
            </Text>
          </View>
        </View>
      )}

      {/* Action Buttons */}
      <View style={styles.section}>
        <TouchableOpacity
          style={styles.directionsButton}
          onPress={handleGetDirections}>
          <Text style={styles.buttonText}>🚗 {t('get_directions')}</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.searchButton}
          onPress={handleSearchGoogle}>
          <Text style={styles.buttonText}>🔍 {t('search_google')}</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.backgroundLight,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.backgroundLight,
  },
  loadingText: {
    marginTop: 10,
    color: colors.textPrimary,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.backgroundLight,
  },
  errorText: {
    color: colors.error,
    fontSize: 16,
  },
  header: {
    backgroundColor: colors.background,
    padding: 20,
    borderBottomWidth: 3,
    borderBottomColor: colors.primary,
  },
  businessName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 10,
  },
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  categoryBadge: {
    backgroundColor: colors.primary,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    marginRight: 8,
    marginBottom: 8,
  },
  categoryText: {
    color: colors.textPrimary,
    fontSize: 13,
    fontWeight: '600',
  },
  infoCard: {
    backgroundColor: colors.background,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  infoText: {
    fontSize: 15,
    color: colors.textSecondary,
  },
  directionsButton: {
    backgroundColor: colors.primary,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  searchButton: {
    backgroundColor: colors.secondary,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  buttonText: {
    color: colors.textPrimary,
    fontSize: 16,
    fontWeight: '600',
  },
});

