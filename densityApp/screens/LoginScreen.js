import React from 'react';
import {SearchBar} from 'react-native-elements';
import HomeCard from '../components/HomeCard.js';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  View,
  Button,
  AsyncStorage,
} from 'react-native';
import { WebBrowser } from 'expo';
import { MonoText } from '../components/StyledText';
import * as Expo from 'expo';
import MainTabNavigator from '../navigation/MainTabNavigator';
import LoginStack from '../navigation/MainTabNavigator';
import HomeStack from '../navigation/MainTabNavigator';
import LinksStack from '../navigation/MainTabNavigator';
import SettingsStack from '../navigation/MainTabNavigator';
import { createStackNavigator, createBottomTabNavigator } from 'react-navigation';

const PUSH_ENDPOINT = 'https://density.adicu.com/users/push-token';

//Creates a token for a given user and stores it in the db
async function registerForPushNotificationsAsync(user_email) {
  const { status: existingStatus } = await Expo.Permissions.getAsync(
    Expo.Permissions.NOTIFICATIONS
  );
  let finalStatus = existingStatus;

  // only ask if permissions have not already been determined, because
  // iOS won't necessarily prompt the user a second time.
  if (existingStatus !== 'granted') {
    // Android remote notification permissions are granted during the app
    // install, so this will only ask on iOS
    const { status } = await Expo.Permissions.askAsync(Expo.Permissions.NOTIFICATIONS);
    finalStatus = status;
  }

  // Stop here if the user did not grant permissions
  if (finalStatus !== 'granted') {
    return;
  }

  // Get the token that uniquely identifies this device
  let token = await Expo.Notifications.getExpoPushTokenAsync();

  // POST the token to your backend server from where you can retrieve it to send push notifications.
  return fetch(PUSH_ENDPOINT, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      token: token,
      user_email: user_email,
    }),
  });
}


_storeData = async () => {
  try {
    await AsyncStorage.setItem('loggedIn', '0');
    console.log("worked");
  } catch (error) {
  }
}

_retrieveData = async () => {
  try {
    const value = await AsyncStorage.getItem('loggedIn');
    if (value !== null) {
      return parseInt(value,10);
    }
  } catch (error) {
  }
}

export default class LoginScreen extends React.Component {

  static navigationOptions = {
    header: null,
  };

    constructor(props) {
        super(props)
        this.state = {signedIn: false, name: "", photoUrl: "",}
    }

    signIn = async () => {
    try {
      const result = await Expo.Google.logInAsync({
        iosClientId: "87562248901-1u80sukceh55jmu08dofb93u6njovh0g.apps.googleusercontent.com",
        scopes: ["profile", "email"]
      })

            if (result.type === "success") {
        this.setState({
          signedIn: true,
          name: result.user.name,
          photoUrl: result.user.photoUrl
        })
        console.log(this.state.name)
      } else {
        console.log("cancelled")
      }

    } catch (e) {
      console.log("error", e)
    }
  }


  render() {

    return (

      <View style={styles.container}>
       			<View style={{
				height: 100,
				backgroundColor: '#2185C6',
				alignItems: 'center'
			}}>

    	<View style={{
    				height: 80,
    				paddingTop: 30,
    				justifyContent: 'center',
    				alignItems: 'center',
    				backgroundColor: '#2185C6'
    			}}>
			   <Image source={require('../assets/images/logo2.png')} resizeMode={'center'} />
			 </View>
			<View style={{
				alignItems: 'center',
				justifyContent: 'center'
			}}>

        {this.state.signedIn ? (
          <LoggedInPage name={this.state.name} photoUrl={this.state.photoUrl} />
        ) : (
          <LoginPage signIn={this.signIn} />
        )}

      </View>
      </View>
      </View>
    );
  }
}


const LoginPage = props => {
  return (
    <View style={{
            paddingTop: '30%',
            justifyContent: 'center',
            alignItems: 'center',
          }}>
    <Text style={{color: '#2185C6', fontSize: 25, fontWeight: 'bold'}}>
        Welcome to the Density App!
    </Text>
    <Text style={{color: '#2185C6', paddingTop: 50, fontSize: 15, fontWeight: 'bold'}}>
       Register with your Columbia Account:
    </Text>

      <TouchableOpacity onPress={() => {props.signIn();}}>

      <Image source={require('../assets/images/google_signin.png')} resizeMode={'center'} />
    </TouchableOpacity>
    </View>
  )
}

const LoggedInPage = props => {
   _storeData();
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Welcome:{props.name}</Text>
      <Image style={styles.image} source={{ uri: props.photoUrl }} />
      
      <TouchableOpacity onPress={() => {_retrieveData(); createBottomTabNavigator(0 ? {
  LoginStack,
  HomeStack,
  LinksStack,
  SettingsStack,
}:{LoginStack,})}}>

      <Image source={require('../assets/images/google_signin.png')} resizeMode={'center'} />
    </TouchableOpacity>


    </View>
  )
}



const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
  fontSize: 25
},
  image: {
  marginTop: 15,
  width: 150,
  height: 150,
  borderColor: "rgba(0,0,0,0.2)",
  borderWidth: 3,
  borderRadius: 150
},
  developmentModeText: {
    marginBottom: 20,
    color: 'rgba(0,0,0,0.4)',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
  },
  body: {
    backgroundColor: '#e2e2e2',
    paddingTop: 15,
    paddingHorizontal: 15,
    lineHeight: 20,
  },
  footer: {
    backgroundColor: '#e2e2e2',
    paddingTop: 15,
    paddingHorizontal: 15,
    lineHeight: 20,
    textAlign: "right",
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 3,
    marginLeft: -10,
  },
  getStartedContainer: {
    alignItems: 'center',
    marginHorizontal: 50,
  },
  homeScreenFilename: {
    marginVertical: 7,
  },
  codeHighlightText: {
    color: 'rgba(96,100,109, 0.8)',
  },
  codeHighlightContainer: {
    backgroundColor: 'rgba(0,0,0,0.05)',
    borderRadius: 3,
    paddingHorizontal: 4,
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  tabBarInfoContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    ...Platform.select({
      ios: {
        shadowColor: 'black',
        shadowOffset: { height: -3 },
        shadowOpacity: 0.1,
        shadowRadius: 3,
      },
      android: {
        elevation: 20,
      },
    }),
    alignItems: 'center',
    backgroundColor: '#fbfbfb',
    paddingVertical: 20,
  },
  tabBarInfoText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    textAlign: 'center',
  },
  navigationFilename: {
    marginTop: 5,
  },
  helpContainer: {
    marginTop: 15,
    alignItems: 'center',
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
});
