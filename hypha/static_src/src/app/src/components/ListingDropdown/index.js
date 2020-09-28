import React from 'react';
import PropTypes from 'prop-types';
import smoothscroll from 'smoothscroll-polyfill';

export default class ListingDropdown extends React.Component {
    static propTypes = {
        listRef: PropTypes.object,
        groups: PropTypes.object,
        scrollOffset: PropTypes.number,
    }

    componentDidMount() {
        // polyfill element.scrollTo
        smoothscroll.polyfill();
    }

    handleChange(e) {
        const groupHeaderPosition = document.getElementById(e.target.value).offsetTop - this.props.scrollOffset;

        this.props.listRef.current.scrollTo({
            top: groupHeaderPosition
        })
    }

    renderListDropdown() {
        const { groups } = this.props;
        return (
            <form className="form form__select">
                <select onChange={(e) => this.handleChange(e)} aria-label="Jump to listing group">
                <optgroup label="filter-by-status">
                    {groups.statuses.map((group, index) => {
                        return (
                            <option key={`listing-heading-${group.key}`} value={group.key} selected={index == 0 && "selected"}>{group.name}</option>
                        )
                    })}
                </optgroup>
                <optgroup label="filter-by-screening">
                    {groups.screening.map(group => {
                        return (
                            <option key={`listing-heading-${group.key}`} value={group.key}>{group.name}</option>
                        )
                    })}
                </optgroup>
                </select>
            </form>
        )
    }

    render() {
        return (
            <>
                {this.renderListDropdown()}
            </>
        )
    }
}
