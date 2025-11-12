/**
 * Berlin Business Finder - Mobile App
 * React Native with TypeScript
 */

import React, {useEffect} from 'react';
import {StatusBar} from 'react-native';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import AppNavigator from './src/navigation/AppNavigator';
import './src/i18n/config';

function App() {
  return (
    <SafeAreaProvider>
      <StatusBar barStyle="dark-content" backgroundColor="#FFD700" />
      <AppNavigator />
    </SafeAreaProvider>
  );
}

export default App;
