import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import PropTypes from 'prop-types';

class HomeCard extends Component {
	constructor(props) {
		super(props);
		// this.handleSearchChange = this.handleSearchChange.bind(this);
	}

	static propTypes = {
		name: PropTypes.string.isRequired,
		closeTime: PropTypes.string.isRequired,
		percentFull: PropTypes.number.isRequired,
	}

  render = () => {
    	const name = this.props.name;
    	const closeTime = this.props.closeTime;
    	const percentFull = this.props.percentFull;
    	const inSearch = this.props.inSearch;
	    return (
	    	<View style={styles.card} style={{display: inSearch }}>
	    		<View style={{flex: 1}}>
	    			<Text>{name}</Text>
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
		flexDirection: 'row',
	},
	percent: {
		fontSize: 24
	}
});

export default HomeCard;