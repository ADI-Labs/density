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
} from 'react-native';
import { WebBrowser, Notifications } from 'expo';

import { MonoText } from '../components/StyledText';


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

class MyButton extends React.Component {
  setNativeProps = (nativeProps) => {
    this._root.setNativeProps(nativeProps);
  }

  render(){
    return (
      <View ref = {component => this._root = component} {...this.props}>
        <Text style = {{ fontSize: 14, color: 'white', textAlign:'center', fontWeight: "100" }}>{this.props.label}</Text>
      </View>
    )
  }
}

export default class HomeScreen extends React.Component {
  constructor(props){
 		 super(props);
 		 this.onLocationChange = this.onLocationChange.bind(this);
 		 this.onOpenChange = this.onOpenChange.bind(this);
 		 this.onSearchChange = this.onSearchChange.bind(this);
 		 this.updateDisplay = this.updateDisplay.bind(this);
 		 this.state = {
       isLoading: true,
       search: "",
       location:  "",
       open: "",
       searchResults: [],
       notification: {}
     }
   }

  static navigationOptions = {
    header: null,
  };

  componentDidMount(){
      registerForPushNotificationsAsync("mark@columbia.edu");

    // Handle notifications that are received or selected while the app
    // is open. If the app was closed and then opened by tapping the
    // notification (rather than just tapping the app icon to open it),
    // this function will fire on the next tick after the app starts
    // with the notification data.
      this._notificationSubscription = Notifications.addListener(this._handleNotification);
      return fetch('https://density.adicu.com/latest?auth_token=JCAhr3xirjnP0O3dEKjTiCLX_uaQCJJ2TWtyMLpjRgNVqhzQuYJEK78-HbBgGCa7')
        .then((response) => response.json())
        .then((responseJson) => {
          this.setState({
            isLoading: false,
            dataSource: responseJson.data
          }, function(){

          });
        })
        .catch((error) => {
          console.error(error);
        });
  }

  _handleNotification = (notification) => {
    this.setState({notification: notification});
  };

  mapBuildings(){
    const building_data = this.state.dataSource;

    for (let i = 0; i < building_data.length; i++) {
      this.state.searchResults.push(
          [building_data[i].group_name, "library", "open", "block"]
      );
    }

    const building_cards = [];

    for (let i = 0; i < building_data.length; i++) {
      building_cards.push(<HomeCard key={i}
                                    name={building_data[i].group_name}
                                    closeTime={building_data[i].dump_time}
                                    percentFull={building_data[i].percent_full}
                                    inSearch={this.state.searchResults[i][3]}></HomeCard>)

    }

    return building_cards;
  }

  onLocationChange(locationFilter) {
    this.setState({location: locationFilter});
    this.updateDisplay();
  }

  onOpenChange(openFilter) {
    this.setState({open: openFilter});
    this.updateDisplay();
  }

  onSearchChange(searchQuery) {
    this.setState({search: searchQuery});
    this.updateDisplay();
  }

  updateDisplay() {
    var searchQuery = this.state.search.toLowerCase();
    var locationFilter = this.state.location;
    var openFilter = this.state.open;

    this.state.searchResults.forEach((kv) => {

      var name = kv[0].toLowerCase();
      var nickname = kv[0].toLowerCase(); // Same as name for fake data
      var locationType = kv[1]; // Always library for fake data
      var openNow = kv[2]; // Always open for fake data

      if((!name.includes(searchQuery) && !nickname.includes(searchQuery)) ||
          (locationFilter != '' && locationFilter != locationType) ||
          (openFilter != '' && openFilter != openNow)) {
        kv[3] = "none";
      } else {
        kv[3] = "block";
      }
    });
  }

  render() {
    const search = this.state.search;
    const locationType = this.state.location;
    const isOpen = this.state.open;

    if(this.state.isLoading){
	 			return (
	 				<View style = {{flex: 1, padding: 20}}>
	 					<ActivityIndicator/>
	 					</View>
	 			)
	 		}

    return (
      <View style={styles.container}>
       			<View style={{
				height: 210,
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
				width:'90%',
				paddingTop: 10,
				alignItems: 'center',
				justifyContent: 'center'

			}}>

			<SearchBar
    			placeholder="search by building"
    			onChangeText={this.onSearchChange}
    			placeholderTextColor='#C1C1C1'
    			value={search}
    			platform="ios"
    			containerStyle={{backgroundColor:'#2185C6'}}
    			inputStyle={{backgroundColor: 'white'}}
    			inputContainerStyle={{backgroundColor: 'white'}}
    			leftIconContainerStyle={{backgroundColor: 'white'}}
    			rightIconContainerStyle={{backgroundColor: 'white'}}
          cancelButtonProps={{color:'white'}}
			/>
			</View>
      <View style={{
        width:'90%',
        flex: 1,
        fontSize: 2,
        textAlign: 'center',
        flexDirection: 'row',
        justifyContent: 'space-evenly',
				height:18,
        backgroundColor: '#2185C6',
			}}>
      <View style = {{flex: 1}}>
      <TouchableOpacity onPress={this.onLocationChange.bind(this, "dining hall")} >
        <MyButton label = "dining hall"/>
      </TouchableOpacity>
      </View>
      <View style = {{flex: 1}}>
      <TouchableOpacity onPress={this.onLocationChange.bind(this, "library")} >
        <MyButton label = "library"/>
      </TouchableOpacity>
      </View>
      <View style = {{flex: 1}} >
      <TouchableOpacity onPress={this.onLocationChange.bind(this, "student center")} >
        <MyButton label = "student center"/>
      </TouchableOpacity>
      </View>
      <View style = {{flex: 1}} >
      <TouchableOpacity onPress={this.onOpenChange.bind(this, "open")} >
        <MyButton label = "open"/>
      </TouchableOpacity>
      </View>
      <View style = {{flex: 1}}>
      <TouchableOpacity onPress={this.onOpenChange.bind(this, "closed")} >
        <MyButton label = "closed"/>
      </TouchableOpacity>
      </View>
      </View>
      </View>
        <ScrollView>
          <View style={styles.body}>
            {this.mapBuildings()}
          </View>
          <View>
            <Text style={ styles.footer }>
              Last updated:{"\n"}
              Maintained by ADI Labs{"\n"}
            </Text>
          </View>
          <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
            <Text>Origin: {this.state.notification.origin}</Text>
            <Text>Data: {JSON.stringify(this.state.notification.data)}</Text>
          </View>
        </ScrollView>

      </View>

    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
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
