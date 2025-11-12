/**
 * App Navigation - Tab and Stack navigation
 */

import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';
import {useTranslation} from 'react-i18next';
import {Text} from 'react-native';

// Screens
import MapScreen from '../screens/MapScreen';
import SearchScreen from '../screens/SearchScreen';
import SettingsScreen from '../screens/SettingsScreen';
import BusinessDetailScreen from '../screens/BusinessDetailScreen';

// Colors
import colors from '../theme/colors';

// Types
export type RootStackParamList = {
  MainTabs: undefined;
  BusinessDetail: {businessId: string};
};

export type TabParamList = {
  Map: undefined;
  Search: undefined;
  Settings: undefined;
};

const Tab = createBottomTabNavigator<TabParamList>();
const Stack = createStackNavigator<RootStackParamList>();

// Tab Navigator
function TabNavigator() {
  const {t} = useTranslation();

  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        tabBarStyle: {
          backgroundColor: colors.background,
          borderTopColor: colors.border,
        },
        headerStyle: {
          backgroundColor: colors.primary,
        },
        headerTintColor: colors.textPrimary,
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}>
      <Tab.Screen
        name="Map"
        component={MapScreen}
        options={{
          title: t('map_tab'),
          tabBarIcon: ({color}) => <Text style={{fontSize: 20}}>🗺️</Text>,
        }}
      />
      <Tab.Screen
        name="Search"
        component={SearchScreen}
        options={{
          title: t('search_tab'),
          tabBarIcon: ({color}) => <Text style={{fontSize: 20}}>🔍</Text>,
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          title: t('settings_tab'),
          tabBarIcon: ({color}) => <Text style={{fontSize: 20}}>⚙️</Text>,
        }}
      />
    </Tab.Navigator>
  );
}

// Main App Navigator
export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="MainTabs"
          component={TabNavigator}
          options={{headerShown: false}}
        />
        <Stack.Screen
          name="BusinessDetail"
          component={BusinessDetailScreen}
          options={{
            title: 'Business Details',
            headerStyle: {
              backgroundColor: colors.primary,
            },
            headerTintColor: colors.textPrimary,
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

