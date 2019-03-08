import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import PropTypes from 'prop-types';
import { VictoryChart, VictoryZoomContainer, VictoryLine, VictoryAxis } from "victory-native";

class PredictCard extends Component {
  	handleZoom(domain) {
	    this.setState({ zoomDomain: domain });
  	}

	static propTypes = {
	    building: PropTypes.string.isRequired,
	    year: PropTypes.number.isRequired,
	    month: PropTypes.number.isRequired,
	    date: PropTypes.number.isRequired,
	    data: PropTypes.arrayOf(PropTypes.array).isRequired
	    // closeTime: PropTypes.string.isRequired,
	    // percentFull: PropTypes.number.isRequired,
	  }

  	// Helper method that creates a Date object out of an int year, int month, int date, and string time
  	parseTime(y, m, d, strTime) {
  		var temp = strTime.split(":");
  		return new Date(y, m, d, parseInt(temp[0]), parseInt(temp[1]));
  	}

	render = () => {
    	const { building, year, month, date, data } = this.props;
    	zoomDomain = { x: [new Date(year, month, date, 6, 0), new Date(year, month, date, 18, 0)] };
    	parseData = [];
    	for (let point of data) {
    		var time = this.parseTime(year, month, date, point[0]);
    		var capacity = point[1];
    		parseData.push({a: time, b: capacity});
    	}
	    return (
	    	<View style={styles.card}>
	    		<Text style={{ paddingHorizontal: 15 }}>{building}</Text>
	    		<View style={styles.chart}>
					<VictoryChart padding={{ top: 15, bottom: 30, left: 50, right: 50 }} height={200} scale={{ x: "time" }}
			          containerComponent={
			            <VictoryZoomContainer
			           	 domain={{ y: [0, 100]}}
			              zoomDimension="x"
			              zoomDomain={zoomDomain}
			              onZoomDomainChange={this.handleZoom.bind(this)}
			            />
			          }
			        >
			        	<VictoryAxis tickCount={3}/>
			        	<VictoryAxis dependentAxis/>
			            <VictoryLine
			              style={{ 
			                data: { stroke: "tomato" }
			              }}
			              data={parseData}
			              x="a"
			              y="b"
			            />

			          </VictoryChart>
	    		</View>
	    	</View>
	    );
	}
}	

const styles = StyleSheet.create({
	card: {
		borderRadius: 10,
		backgroundColor: '#fff',
		paddingVertical: 15,
		marginBottom: 15,
		flexDirection: 'column'
	},
	chart: {
	}
});

export default PredictCard;