import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import PropTypes from 'prop-types';

class PredictCard extends Component {
	static propTypes = {
	    building: PropTypes.string.isRequired,
	    // closeTime: PropTypes.string.isRequired,
	    // percentFull: PropTypes.number.isRequired,
	  }

	render = () => {
    	const { building } = this.props;
	    return (
	    	<View style={styles.card}>
	    		<Text>{building}</Text>
	    		<View>
	    			<Text>graph goes here</Text>
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
		flexDirection: 'column'
	},
});

export default PredictCard;