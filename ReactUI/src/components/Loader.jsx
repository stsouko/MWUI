import React, { Fragment } from 'react';
import PropTypes from 'prop-types';
import { Spin, Button } from 'antd';


const Loader = ({ loading, children }) => (
  <Spin
    size="large"
    tip="Loading..."
    spinning={loading}
  >
    { children }
  </Spin>
);

Loader.propTypes = {
  loading: PropTypes.bool,
};

Loader.defaultProps = {
  loading: false,
};

export default Loader;
