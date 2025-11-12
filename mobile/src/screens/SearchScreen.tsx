/**
 * Search Screen - List view with filters
 */

import React, {useState, useEffect} from 'react';
import {
  View,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Text,
  FlatList,
  ActivityIndicator,
} from 'react-native';
import {Picker} from '@react-native-picker/picker';
import {useTranslation} from 'react-i18next';
import {useNavigation} from '@react-navigation/native';
import ApiService, {Business} from '../services/api';
import colors from '../theme/colors';

export default function SearchScreen() {
  const {t} = useTranslation();
  const navigation = useNavigation();
  
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  
  const [categories, setCategories] = useState<string[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCity, setSelectedCity] = useState('');

  useEffect(() => {
    loadFilters();
    loadBusinesses();
  }, []);

  const loadFilters = async () => {
    try {
      const [categoriesData, citiesData] = await Promise.all([
        ApiService.getCategories(),
        ApiService.getCities(),
      ]);
      setCategories(categoriesData);
      setCities(citiesData);
    } catch (error) {
      console.error('Error loading filters:', error);
    }
  };

  const loadBusinesses = async () => {
    setLoading(true);
    try {
      const response = await ApiService.getBusinesses({
        search: searchText || undefined,
        category: selectedCategory || undefined,
        city: selectedCity || undefined,
        limit: 50,
      });
      setBusinesses(response.businesses);
    } catch (error) {
      console.error('Error loading businesses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSearchText('');
    setSelectedCategory('');
    setSelectedCity('');
  };

  const renderBusinessItem = ({item}: {item: Business}) => (
    <TouchableOpacity
      style={styles.businessCard}
      onPress={() =>
        navigation.navigate('BusinessDetail' as never, {businessId: item.id} as never)
      }>
      <Text style={styles.businessName}>{item.name}</Text>
      
      <View style={styles.categoriesContainer}>
        {item.categories.slice(0, 2).map((cat, index) => (
          <View key={index} style={styles.categoryBadge}>
            <Text style={styles.categoryText}>{cat}</Text>
          </View>
        ))}
      </View>
      
      <Text style={styles.businessLocation}>
        📍 {item.postal_code} {item.city}
      </Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Search Input */}
      <View style={styles.searchSection}>
        <TextInput
          style={styles.searchInput}
          placeholder={t('search_placeholder')}
          value={searchText}
          onChangeText={setSearchText}
        />
      </View>

      {/* Filters */}
      <View style={styles.filtersSection}>
        <View style={styles.pickerContainer}>
          <Text style={styles.filterLabel}>{t('filter_category')}</Text>
          <Picker
            selectedValue={selectedCategory}
            onValueChange={setSelectedCategory}
            style={styles.picker}>
            <Picker.Item label={t('all_categories')} value="" />
            {categories.slice(0, 50).map(cat => (
              <Picker.Item key={cat} label={cat} value={cat} />
            ))}
          </Picker>
        </View>

        <View style={styles.pickerContainer}>
          <Text style={styles.filterLabel}>{t('filter_city')}</Text>
          <Picker
            selectedValue={selectedCity}
            onValueChange={setSelectedCity}
            style={styles.picker}>
            <Picker.Item label={t('all_cities')} value="" />
            {cities.slice(0, 50).map(city => (
              <Picker.Item key={city} label={city} value={city} />
            ))}
          </Picker>
        </View>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity
          style={[styles.button, styles.searchButton]}
          onPress={loadBusinesses}>
          <Text style={styles.buttonText}>{t('search_button')}</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.button, styles.resetButton]}
          onPress={handleReset}>
          <Text style={styles.buttonText}>{t('reset_filters')}</Text>
        </TouchableOpacity>
      </View>

      {/* Results List */}
      {loading ? (
        <View style={styles.loadingCenter}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      ) : (
        <FlatList
          data={businesses}
          renderItem={renderBusinessItem}
          keyExtractor={item => item.id}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>🔍</Text>
              <Text style={styles.emptySubtext}>{t('no_results')}</Text>
            </View>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.backgroundLight,
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
    marginBottom: 10,
  },
  filterLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 5,
  },
  picker: {
    height: 50,
    borderWidth: 1,
    borderColor: colors.border,
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
  searchButton: {
    backgroundColor: colors.primary,
  },
  resetButton: {
    backgroundColor: colors.border,
  },
  buttonText: {
    color: colors.textPrimary,
    fontWeight: '600',
    fontSize: 14,
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
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 16,
    color: colors.textSecondary,
  },
});

