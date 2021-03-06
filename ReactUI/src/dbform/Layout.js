import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Tabs, Icon, Spin } from 'antd';
import {
  CreatePage,
  StructureListPage,
  SettingsPage,
  InfoPage,
} from './components';
import { LoaderView, ErrorView } from '../base/wrapper';
import { MainLayout } from '../components';
import { DBFormModalView } from './components';
import { getSettings } from './core/selectors';

const TabPane = Tabs.TabPane;

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeKey: '',
    };
    this.changeTab = this.changeTab.bind(this);
  }

  changeTab(activeKey) {
    this.setState({ activeKey });
  }

  render() {
    const { settings } = this.props;
    const tabs = settings && settings.tabs;
    const { activeKey } = this.state;

    return (
      <LoaderView>
        <MainLayout>
          <ErrorView />
          <DBFormModalView />

          <Tabs
            defaultActiveKey="2"
            onChange={this.changeTab}
            {...tabs}
          >
            <TabPane tab={<span><Icon type="file-add" />Create</span>} key="1">
              <CreatePage active={activeKey === '1'} />
            </TabPane>
            <TabPane tab={<span><Icon type="database" />List</span>} key="2">
              <StructureListPage active={activeKey === '2'} />
            </TabPane>
            <TabPane tab={<span><Icon type="setting" />Settings</span>} key="3">
              <SettingsPage active={activeKey === '3'} />
            </TabPane>
            <TabPane tab={<span><Icon type="info-circle-o" />Info</span>} key="4">
              <InfoPage active={activeKey === '4'} />
            </TabPane>
          </Tabs>
        </MainLayout>
      </LoaderView>
    );
  }
}

const mapStateToProps = state => ({
  settings: getSettings(state),
});


export default connect(mapStateToProps)(Main);
