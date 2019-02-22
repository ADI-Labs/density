import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import PropTypes from 'prop-types';
import PureChart from 'react-native-pure-chart';

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
	    		<View style={styles.chart}>
					  <PureChart data={[
					      {x: '12:30', y: 50},
					      {x: '1:00', y: 40},
					      {x: '1:30', y: 50},
					      {x: '2:00', y: 70},
					      {x: '2:30', y: 60},
					      {x: '3:00', y: 30}
					  ]} type='line' />
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
	chart: {
		paddingTop: 15
	}
});

export default PredictCard;