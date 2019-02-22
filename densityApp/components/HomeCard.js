import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import PropTypes from 'prop-types';

class HomeCard extends Component {
	static propTypes = {
	    building: PropTypes.string.isRequired,
	    closeTime: PropTypes.string.isRequired,
	    percentFull: PropTypes.number.isRequired,
	  }

	render = () => {
    	const { building, closeTime, percentFull } = this.props;
	    return (
	    	<View style={styles.card}>
	    		<View style={{flex: 1}}>
	    			<Text>{building}</Text>
		    		<Text style={{color:'#f9725e'}}>(closes at {closeTime})</Text>
	    		</View>
	    		<View style={{justifyContent: 'center', alignItems: 'center'}}>
	    			<Text style={{color: '#2185C6'}}><Text style={styles.percent}>{percentFull}%</Text> full</Text>
	    		</View>
	    	</View>
	    );
	}
}	

const styles = StyleSheet.create({
	card: {
		borderRadius: 10,
		backgroundColor: '#fff',
		padding: 15,
		marginBottom: 15,
		flexDirection: 'row'
	},
	percent: {
		fontSize: 24
	}
});

export default HomeCard;