import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import PropTypes from 'prop-types';

class HomeCard extends Component {
	constructor(props) {
	  super(props);
		this.state = {display: "block"};
	}

	static propTypes = {
		name: PropTypes.string.isRequired,
    nickname: PropTypes.string.isRequired,
    locationType: PropTypes.string.isRequired,
		closeTime: PropTypes.string.isRequired,
		percentFull: PropTypes.number.isRequired,
    searchQuery: PropTypes.string.isRequired,
    locationFilter: PropTypes.string.isRequired,
    openFilter: PropTypes.string.isRequired,
	};

	componentDidUpdate(prevProps) {
	  if(this.props.searchQuery != prevProps.searchQuery
        || this.props.locationFilter != prevProps.locationFilter
        || this.props.openFilter != prevProps.openFilter) {
      var searchQuery = this.props.searchQuery.toLowerCase();
      var locationFilter = this.props.locationFilter.toLowerCase();
      var openFilter = this.props.openFilter.toLowerCase();

      var name = this.props.name.toLowerCase();
      var nickname = this.props.name.toLowerCase(); // Same as name for fake data
      var locationType = this.props.locationType; // Always library for fake data
      var openNow = "open"; // Always open for fake data

      if ((!name.includes(searchQuery) && !nickname.includes(searchQuery)) ||
          (locationFilter != '' && locationFilter != locationType) ||
          (openFilter != '' && openFilter != openNow)) {
        this.setState({display: "none"});
      } else {
        this.setState({display: "block"});
      }
    }
  }

  render = () => {
	    return (
	    	<View style={{display: this.state.display}}>
		    	<View style={styles.card}>
		    		<View style={{flex: 1}}>
		    			<Text>{this.props.name}</Text>
			    		<Text style={{color:'#f9725e'}}>(closes at {this.props.closeTime})</Text>
		    		</View>
		    		<View style={{justifyContent: 'center', alignItems: 'center'}}>
		    			<Text style={{color: '#2185C6'}}><Text style={styles.percent}>{this.props.percentFull}%</Text> full</Text>
		    		</View>
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