import React from 'react';
import {
  ActivityIndicator,
  AsyncStorage,
  StatusBar,
  StyleSheet,
  View,
} from 'react-native';

class AuthLoadingScreen extends React.Component {
  constructor(props) {
    super(props);
    this._retrieveData();
  }


_retrieveData = async () => {
  const userToken = await AsyncStorage.getItem('loggedIn');
  this.props.navigation.navigate(parseInt(userToken,10) ? 'Main' : 'Auth');
}

_storeData = async () => {
  try {
    await AsyncStorage.setItem('loggedIn', '0');
  } catch (error) {
  }
}

  render() {
    return (
      <View>
        <ActivityIndicator />
        <StatusBar barStyle="default" />
      </View>
    );
  }
}

export default AuthLoadingScreen