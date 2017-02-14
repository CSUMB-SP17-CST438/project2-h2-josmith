import * as React from 'react';

import { MyFavoriteAnimalList } from './MyFavoriteAnimalList';

export class Content extends React.Component {
    render() {
        let my_animals = ['cow', 'zebra', 'goat', 'llama'];
        return <MyFavoriteAnimalList animals={my_animals} />
        				<form onSubmit={this.handleSubmit}>
					<input
						onChange={this.onKey}
						value={this.state.newName} 
					/>
				</form>	;
    }
}