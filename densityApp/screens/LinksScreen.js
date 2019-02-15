import React from 'react';
import { FlatList, ActivityIndicator, Text, View } from 'react-native';

export default class APICall extends React.Component {

	constructor(props){
		super(props);
		this.state = {isLoading : true}
	}

	componentDidMount(){
		return fetch('https://density.adicu.com/latest?auth_token=JCAhr3xirjnP0O3dEKjTiCLX_uaQCJJ2TWtyMLpjRgNVqhzQuYJEK78-HbBgGCa7')
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
	render() {

		if(this.state.isLoading){
			return (
				<View style = {{flex: 1, padding: 20}}>
					<ActivityIndicator/>
					</View>
			)
		}

		return(
			<View style={{flex: 1, paddingTop: 20}}>
				<FlatList
					data = {this.state.dataSource}
					renderItem = {({item}) => <Text>{item.building_name}, {item.client_count}, {item.percent_full}</Text>}
					KeyExtractor = {({id}, index) => id}
					/>
					</View>
		);
	}
}
