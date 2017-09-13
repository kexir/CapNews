/**
 * Created by lyuqi on 5/1/17.
 */
import React from 'react';
import RTChart from 'react-rt-chart';

class Chart extends React.Component {
    componentDidMount() {
        setInterval(() => this.forceUpdate(), 1000);
    }
    render() {

        let flow = {
            duration: 200
        };
        let data = {
            date: new Date(),
            name_1: 100,
            name_2: 200
        };

        return (
            <div>
                <RTChart
                    flow={flow}
                    fields={['name_1', 'name_2']}
                    data={data} />
            </div>

        )
    }
}

export default Chart;