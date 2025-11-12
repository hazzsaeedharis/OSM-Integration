/**
 * Map Screen - Main screen with OpenStreetMap and business markers
 */

import React, {useState, useEffect} from 'react';
import {
  View,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Text,
  ActivityIndicator,
  Modal,
  ScrollView,
  Linking,
} from 'react-native';
import MapView, {Marker, PROVIDER_DEFAULT} from 'react-native-maps';
import {useTranslation} from 'react-i18next';
import ApiService, {Business} from '../services/api';
import colors from '../theme/colors';

const BERLIN_CENTER = {
  latitude: 52.52,
  latitudeDelta: 0.3,
  longitude: 13.405,
  longitudeDelta: 0.3,
};

export default function MapScreen() {
  const {t} = useTranslation();
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [selectedBusiness, setSelectedBusiness] = useState<Business | null>(null);
  const [modalVisible, setModalVisible] = useState(false);

  // Load initial businesses
  useEffect(() => {
    loadBusinesses();
  }, []);

  const loadBusinesses = async (search?: string) => {
    setLoading(true);
    try {
      const response = await ApiService.getBusinesses({
        search: search || searchText,
        limit: 100,
      });
      setBusinesses(response.businesses.filter(b => b.lat && b.lon));
    } catch (error) {
      console.error('Error loading businesses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    loadBusinesses(searchText);
  };

  const handleMarkerPress = (business: Business) => {
    setSelectedBusiness(business);
    setModalVisible(true);
  };

  const handleGetDirections = () => {
    if (selectedBusiness?.lat && selectedBusiness?.lon) {
      const url = `https://www.google.com/maps/search/?api=1&query=${selectedBusiness.lat},${selectedBusiness.lon}`;
      Linking.openURL(url);
    }
  };

  const handleSearchGoogle = () => {
    if (selectedBusiness) {
      const query = encodeURIComponent(
        `${selectedBusiness.name} ${selectedBusiness.postal_code} ${selectedBusiness.city}`,
      );
      const url = `https://www.google.com/search?q=${query}`;
      Linking.openURL(url);
    }
  };

  return (
    <View style={styles.container}>
      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder={t('search_placeholder')}
          value={searchText}
          onChangeText={setSearchText}
          onSubmitEditing={handleSearch}
        />
        <TouchableOpacity style={styles.searchButton} onPress={handleSearch}>
          <Text style={styles.searchButtonText}>🔍</Text>
        </TouchableOpacity>
      </View>

      {/* Map */}
      <MapView
        style={styles.map}
        provider={PROVIDER_DEFAULT}
        initialRegion={BERLIN_CENTER}
        showsUserLocation
        showsMyLocationButton>
        {businesses.map(business => (
          <Marker
            key={business.id}
            coordinate={{
              latitude: business.lat!,
              longitude: business.lon!,
            }}
            title={business.name}
            description={business.city}
            pinColor={colors.markerOrange}
            onPress={() => handleMarkerPress(business)}
          />
        ))}
      </MapView>

      {/* Loading Indicator */}
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={styles.loadingText}>{t('loading')}</Text>
        </View>
      )}

      {/* Results Count */}
      {!loading && businesses.length > 0 && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsText}>
            📊 {businesses.length} {t('businesses')}
          </Text>
        </View>
      )}

      {/* Business Detail Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <ScrollView>
              {selectedBusiness && (
                <>
                  {/* Business Name */}
                  <Text style={styles.businessName}>
                    {selectedBusiness.name}
                  </Text>

                  {/* Categories */}
                  <View style={styles.categoriesContainer}>
                    {selectedBusiness.categories.slice(0, 3).map((cat, index) => (
                      <View key={index} style={styles.categoryBadge}>
                        <Text style={styles.categoryText}>{cat}</Text>
                      </View>
                    ))}
                  </View>

                  {/* Location */}
                  <View style={styles.infoSection}>
                    <Text style={styles.infoLabel}>📍 {t('location')}:</Text>
                    <Text style={styles.infoText}>
                      {selectedBusiness.postal_code} {selectedBusiness.city}
                    </Text>
                  </View>

                  {/* Coordinates */}
                  <View style={styles.infoSection}>
                    <Text style={styles.infoLabel}>🗺️ {t('coordinates')}:</Text>
                    <Text style={styles.infoText}>
                      {selectedBusiness.lat?.toFixed(6)}, {selectedBusiness.lon?.toFixed(6)}
                    </Text>
                  </View>

                  {/* Action Buttons */}
                  <View style={styles.buttonContainer}>
                    <TouchableOpacity
                      style={styles.directionsButton}
                      onPress={handleGetDirections}>
                      <Text style={styles.buttonText}>
                        🚗 {t('get_directions')}
                      </Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={styles.searchGoogleButton}
                      onPress={handleSearchGoogle}>
                      <Text style={styles.buttonText}>
                        🔍 {t('search_google')}
                      </Text>
                    </TouchableOpacity>
                  </View>
                </>
              )}
            </ScrollView>

            {/* Close Button */}
            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => setModalVisible(false)}>
              <Text style={styles.closeButtonText}>{t('close')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  searchContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: colors.background,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  searchInput: {
    flex: 1,
    height: 45,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    paddingHorizontal: 15,
    backgroundColor: colors.background,
    fontSize: 16,
  },
  searchButton: {
    width: 45,
    height: 45,
    backgroundColor: colors.primary,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 10,
  },
  searchButtonText: {
    fontSize: 20,
  },
  map: {
    flex: 1,
  },
  loadingContainer: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{translateX: -50}, {translateY: -50}],
    backgroundColor: colors.background,
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  loadingText: {
    marginTop: 10,
    color: colors.textPrimary,
  },
  resultsContainer: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    backgroundColor: colors.background,
    padding: 10,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  resultsText: {
    color: colors.textPrimary,
    fontWeight: '600',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: colors.overlay,
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: colors.background,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
    maxHeight: '70%',
  },
  businessName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.textPrimary,
    marginBottom: 15,
    borderBottomWidth: 2,
    borderBottomColor: colors.primary,
    paddingBottom: 10,
  },
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 15,
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
    fontSize: 12,
    fontWeight: '600',
  },
  infoSection: {
    backgroundColor: colors.backgroundDark,
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
  },
  infoLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: 5,
  },
  infoText: {
    fontSize: 13,
    color: colors.textSecondary,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 15,
  },
  directionsButton: {
    flex: 1,
    backgroundColor: colors.primary,
    padding: 12,
    borderRadius: 8,
    marginRight: 5,
    alignItems: 'center',
  },
  searchGoogleButton: {
    flex: 1,
    backgroundColor: colors.secondary,
    padding: 12,
    borderRadius: 8,
    marginLeft: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: colors.textPrimary,
    fontWeight: '600',
    fontSize: 14,
  },
  closeButton: {
    marginTop: 15,
    padding: 12,
    backgroundColor: colors.border,
    borderRadius: 8,
    alignItems: 'center',
  },
  closeButtonText: {
    color: colors.textPrimary,
    fontWeight: '600',
  },
});

