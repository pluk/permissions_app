import React, { Component } from 'react';
import { Container, List, Form, Image, Header } from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'

import ApiClient from './ApiClient';
import { API_HOST } from './constants';

const queryString = require('query-string');


class App extends Component {
  constructor() {
    super();

    this.appId = null;
    this.APIClient = new ApiClient(API_HOST);

    this.state = {
        permissions: [],
        url: ''
    };
  }

  render() {
    const url = this.state.url

    return (
      <Container text>
        <Header as='h2'>PermissionsApp</Header>
        <Form onSubmit={this.handleGetPermissions}>
          <Form.Input
              placeholder='url...'
              name='url'
              value={url}
              onChange={this.handleChange}
            />
            <Form.Button content='Search' />
        </Form>

        {this._renderList(this.state.permissions)}

      </Container>
    );
  }

  handleChange = (e, { name, value }) => this.setState({ [name]: value })

  handleGetPermissions = (e) => {
    this.setState({
      permissions: []
    });
    var parsedUrl = queryString.parseUrl(this.state.url)

    if (!('id' in parsedUrl.query)) {
      return '';
    }

    var hl = parsedUrl.query.hl || 'en'

    this.APIClient.get(
        '/permissions',
        'appId=' + parsedUrl.query.id + '&hl=' + hl
    )
        .then((response) => {
            this.setState({
                permissions: response.data.permissions
            });
        });
  };

  _renderList = (permissions) => {
    if (permissions.length === 0) {
      return '';
    }

    return (
      <List>
        {permissions.map((permission, i) => { return (this._renderPermission(permission, i))})}
      </List>
    );
  };

  _renderPermission = (permission, i) => {
    return (
      <List.Item key={i}>
        <Image style={{'fontSize':10}} avatar src={permission.picture}/>
        <List.Content>
          <List.Header>{ permission.title }</List.Header>
          <List bulleted>
            {permission.permissions.map((perm, j) => { return (<List.Item key={j}><List.Description>{perm}</List.Description></List.Item>) })}
          </List>
        </List.Content>
      </List.Item>
    );
  };
}

export default App;
