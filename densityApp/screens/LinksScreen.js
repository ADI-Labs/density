import React from 'react';
import {SearchBar} from 'react-native-elements';
import PredictCard from '../components/PredictCard.js';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  View,
  TextInput
} from 'react-native';
import { WebBrowser } from 'expo';

import { MonoText } from '../components/StyledText';

import Svg,{
    Circle,
    Ellipse,
    G,
    TSpan,
    TextPath,
} from 'react-native-svg';

import ModalSelector from 'react-native-modal-selector';

class MyButton extends React.Component {
  setNativeProps = (nativeProps) => {
    this._root.setNativeProps(nativeProps);
  }

  render(){
    return (
      <View ref = {component => this._root = component} {...this.props}>
        <Text style = {{ fontSize: 14, color: 'white', textAlign:'center', fontWeight: '100'}}>{this.props.label}</Text>
      </View>
    )
  }
}

export default class APICall extends React.Component {

  constructor(props){
 		 super(props);
	 		this.state = {
	 			isLoading : true,
				search: '',
				datePicker: '3/1/2019' // Initialize the date displayed on the prediction graphs as today's date.
			}
	 	}

    componentDidMount(){
        //Need to replace this with API for predictions
  	 		return fetch('http://160.39.175.250:80/latest_predict')
  	 			.then((response) => response.json())
  	 			.then((responseJson) => {

  	 				this.setState({
  	 					isLoading: false,
  	 					dataSource: responseJson.data,
  	 				}, function(){

  	 				});
  	 			})
  	 			.catch((error) => {
  	 				console.error(error);
  	 			});
  	}

	static navigationOptions = {
		header: null,
	};

	updateSearch = search => {
		this.setState({ search });
	};

	// Variable for holding all data of all buildings for some number of days
  	data = {
  		"Building 1" : {
  			"3/1/2019": [["01:30",60], ["12:30",90], ["18:30",80]],
  			"3/2/2019": [["01:30",30], ["12:30",60], ["18:30",40]]
  		},
  		"Building 2": {
  			"3/1/2019": [["01:30",60], ["12:30",90], ["18:30",80]],
  			"3/2/2019": [["01:30",30], ["12:30",60], ["18:30",40]]
  		},
  		"Building 3": {
  			"3/1/2019": [["01:30",60], ["12:30",90], ["18:30",80]],
  			"3/2/2019": [["01:30",30], ["12:30",60], ["18:30",40]]
  		},
  	};

  	// Helper method that parses date string of the form "mm/dd/yyyy" into array holding int values of [M, D, Y]
  	parseDate(date) {
  		var temp = date.split("/");
  		return [parseInt(temp[0]), parseInt(temp[1]), parseInt(temp[2])];
  	}

	render() {
		// Generate the dates for the date picker by looking at which dates are present in our data.
		pickerItems = [];
		for (var buildingKey in this.data) {
			let index = 0;
			for (var dateKey in this.data[buildingKey]) {
				pickerItems.push({key: index++, label: dateKey})
			}
			break;
		}

		// Extract capacity data for each building for a given date and create PredictCard components to display.
		charts = [];
		var dateArr = this.parseDate(this.state.datePicker);
		for (var key in this.data) {
			var building = key;
			var points = this.data[key][this.state.datePicker]; // Get the current day's data points for this given building
			charts.push(<PredictCard building={key} year={dateArr[2]} month={dateArr[0]} date={dateArr[1]} data={points}></PredictCard>);
		}

		const { search } = this.state;
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
						paddingTop: '9%',
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
					onChangeText={this.updateSearch}
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
			<TouchableOpacity>
				<MyButton label = "dining hall"/>
			</TouchableOpacity>
			</View>
			<View style = {{flex: 1}}>
			<TouchableOpacity>
				<MyButton label = "library" />
			</TouchableOpacity>
			</View>
			<View style = {{flex: 1}} >
			<TouchableOpacity>
				<MyButton label = "student center"/>
			</TouchableOpacity>
			</View>
			<View style = {{flex: 1}}>
			<TouchableOpacity>
				<MyButton label = "open now"/>
			</TouchableOpacity>
			</View>
			<View style = {{flex: 1}}>
			<TouchableOpacity>
				<MyButton label = "closed"/>
			</TouchableOpacity>
			</View>
			</View>
			</View>

				<ScrollView>
		            <ModalSelector
	                    data={pickerItems}
	                    initValue={this.state.datePicker}
	                    onChange={(option)=>{ this.setState({datePicker: option.label})}}
	                    style={styles.datePickerWrap}>

	                    <TextInput
	                        style={styles.datePicker}
	                        editable={false}
	                        placeholder={'Select date.'}
	                        value={'Viewing predictions for: ' + this.state.datePicker} />

	                </ModalSelector>
					<View style={styles.body}>
						{ charts }
					</View>
					<View>
						<Text style={ styles.footer }>
							Last updated:{"\n"}
							Maintained by ADI Labs{"\n"}
						</Text>
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
	datePickerWrap: {
		backgroundColor: '#e2e2e2',
		paddingHorizontal: 15,
		paddingTop: 15
	},
	datePicker: {
		backgroundColor: 'white',
		borderWidth:1, borderColor:'#ccc', padding:15, height:30
	}
	});
