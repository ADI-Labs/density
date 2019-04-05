import React from 'react';
import { ExpoConfigView } from '@expo/samples';

import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  View,
} from 'react-native';
import { WebBrowser } from 'expo';

import { MonoText } from '../components/StyledText';

import ModalSelector from 'react-native-modal-selector';

export default class SettingsScreen extends React.Component {
	constructor(props) {
        super(props);

        this.state = {
	       isLoading: true,
        }
    }

	static navigationOptions = {
		header: null,
	};

	componentDidMount(){
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

	// mapLibraries() {
	// 	const building_data = this.state.dataSource;
	//     const libraries = [];
	//     for (let i = 0; i < building_data.length; i++) {
	//       libraries.push({key: i, label: building_data[i].group_name});
	//     }
	//     return libraries;
	// }

  render() {
  	const diningHalls = [
  		{key: 0, label: 'John Jay'},
  		{key: 1, label: 'JJ\'s'}
  	];

  	const libraries = [
  		{key: 0, label: 'Avery'},
  		{key: 1, label: 'Uris'}
  	];

  	const times = [
  		{key: 0, label: '12:00 am'},
  		{key: 1, label: '1:00 am'},
  		{key: 2, label: '2:00 am'},
  		{key: 3, label: '3:00 am'},
  		{key: 4, label: '4:00 am'},
  		{key: 5, label: '5:00 am'},
  		{key: 6, label: '6:00 am'},
  		{key: 7, label: '7:00 am'},
  		{key: 8, label: '8:00 am'},
  		{key: 9, label: '9:00 am'},
  		{key: 10, label: '10:00 am'},
  		{key: 11, label: '11:00 am'},
  		{key: 12, label: '12:00 pm'},
  		{key: 13, label: '1:00 pm'},
  		{key: 14, label: '2:00 pm'},
  		{key: 15, label: '3:00 pm'},
  		{key: 16, label: '4:00 pm'},
  		{key: 17, label: '5:00 pm'},
  		{key: 18, label: '6:00 pm'},
  		{key: 19, label: '7:00 pm'},
  		{key: 20, label: '8:00 pm'},
  		{key: 21, label: '9:00 pm'},
  		{key: 22, label: '10:00 pm'},
  		{key: 23, label: '11:00 pm'},
  	];
    return (
    	<View style={styles.container}>
    		<View style={{
    				height: 80,
    				paddingVertical: 55,
    				justifyContent: 'center',
    				alignItems: 'center',
    				backgroundColor: '#2185C6'
    			}}>
			   	<Image source={require('../assets/images/logo2.png')} resizeMode={'center'} />
			</View>
			<ScrollView>
	          <View style={styles.body}>

	            <View style={styles.card}>
		    		<View style={{flex: 1}}>
		    			<Text>Favorite dining hall?</Text>
		    			<ModalSelector
		                    data={diningHalls}
		                    initValue={this.state.diningHallVal}
		                    onChange={(option)=>{ this.setState({diningHallVal: option.label})}}
		                    style={{ paddingVertical: 10 }}>
		                    <TextInput
		                        style={{borderWidth:1, borderColor:'#ccc', padding:10, height:30}}
		                        editable={false}
		                        placeholder="Yum."
		                        value={this.state.diningHallVal}/>
		                </ModalSelector>
		    		</View>
		    		<View style={{flex: 1}}>
		    			<Text>When would you prefer to come here?</Text>
		    			<ModalSelector
		                    data={times}
		                    initValue={this.state.diningHallStart}
		                    onChange={(option)=>{ this.setState({diningHallStart: option.label})}}
		                    style={{ paddingVertical: 10 }}>
		                    <TextInput
		                        style={{borderWidth:1, borderColor:'#ccc', padding:10, height:30}}
		                        editable={false}
		                        placeholder="From"
		                        value={this.state.diningHallStart}/>
		                </ModalSelector>
		                <ModalSelector
		                    data={times}
		                    initValue={this.state.diningHallEnd}
		                    onChange={(option)=>{ this.setState({diningHallEnd: option.label})}}>
		                    <TextInput
		                        style={{borderWidth:1, borderColor:'#ccc', padding:10, height:30}}
		                        editable={false}
		                        placeholder="To"
		                        value={this.state.diningHallEnd}/>
		                </ModalSelector>
		    		</View>
		    	</View>

		    	<View style={styles.card}>
		    		<View style={{flex: 1}}>
		    			<Text>Favorite library?</Text>
		    			<ModalSelector
		                    data={libraries}
		                    initValue={this.state.libVal}
		                    onChange={(option)=>{ this.setState({libVal: option.label})}}
		                    style={{ paddingVertical: 10 }}>
		                    <TextInput
		                        style={{borderWidth:1, borderColor:'#ccc', padding:10, height:30}}
		                        editable={false}
		                        placeholder="Yum."
		                        value={this.state.libVal}/>
		                </ModalSelector>
		    		</View>
		    		<View style={{flex: 1}}>
		    			<Text>When would you prefer to come here?</Text>
		    			<ModalSelector
		                    data={times}
		                    initValue={this.state.libValStart}
		                    onChange={(option)=>{ this.setState({libValStart: option.label})}}
		                    style={{ paddingVertical: 10 }}>
		                    <TextInput
		                        style={{borderWidth:1, borderColor:'#ccc', padding:10, height:30}}
		                        editable={false}
		                        placeholder="From"
		                        value={this.state.libValStart}/>
		                </ModalSelector>
		                <ModalSelector
		                    data={times}
		                    initValue={this.state.libValEnd}
		                    onChange={(option)=>{ this.setState({libValEnd: option.label})}}>
		                    <TextInput
		                        style={{borderWidth:1, borderColor:'#ccc', padding:10, height:30}}
		                        editable={false}
		                        placeholder="To"
		                        value={this.state.libValEnd}/>
		                </ModalSelector>
		    		</View>
		    	</View>

	          </View>
	          <View>
	            <Text style={ styles.footer }>
	              Last updated:{"\n"}
	              Maintained by ADI Labs{"\n"}
	            </Text>
	          </View>
	        </ScrollView>
		</View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
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
  card: {
	borderRadius: 10,
	backgroundColor: '#fff',
	padding: 15,
	marginBottom: 15,
	flexDirection: 'column'
  },
});