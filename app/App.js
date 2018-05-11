import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import {ToastAndroid} from "react-native";
import { PermissionsAndroid } from 'react-native';
import {Alert} from "react-native";
import NFC, {NfcDataType, NdefRecordType} from "react-native-nfc";
import LightLineService from "./lightline_service";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.version = "v0.14";
    this.service_api = new LightLineService();
    this.user_token = null;
  }
  render() {
    return (
      <View style={styles.container}>
        <Text>lightline {this.version}</Text>
        <Text>Shake your phone to open the developer menu.</Text>
      </View>
    );
  }
  componentDidMount() {
    this.service_api.register().then(response => this.user_token = response.data);
    this.requestNfcPermission().then(result => {
      if (result === true) {
        // ToastAndroid.show("NFC permission granted", ToastAndroid.SHORT);
        this.bindNfcListener();
      } else {
        ToastAndroid.show("NFC permission denied, please allow the Light Line to access NFC", ToastAndroid.SHORT);
      }
    });
  }
  bindNfcListener() {
    NFC.addListener((payload) => {
      switch (payload.type) {
          case NfcDataType.NDEF:
              let messages = payload.data;
              for (let i in messages) {
                  let records = messages[i];
                  for (let j in records) {
                      let r = records[j];
                      if (r.type === NdefRecordType.TEXT) {
                          ToastAndroid.show(r.data);
                          Alert.alert(
                            'Start Ride',
                            'Ride code '+r.data,
                            [
                              {text: 'OK', onPress: () => {
                                console.log('OK Pressed');
                                this.initiateRide(r.data);                                
                              }},
                              {text: 'cancel', onPress: () => console.log('Canceled')},
                            ],
                            { cancelable: false }
                          );
                      } else {
                          ToastAndroid.show(
                              `Non-TEXT tag of type ${r.type} with data ${r.data}`,
                              ToastAndroid.SHORT
                          );
                      }
                  }
              }
              break;
          case NfcDataType.TAG:
              ToastAndroid.show(
                  `The TAG is non-NDEF:\n\n${payload.data.description}`,
                  ToastAndroid.SHORT
              );
              break;
      }
    });
    // ToastAndroid.show("Added nfc listener", ToastAndroid.SHORT);
  }
  async requestNfcPermission() {
    try {
      const granted = await PermissionsAndroid.request("android.permission.NFC",
      {'title':"Light Line NFC Permission",
        'message':"Light Line needs access to your NFC so you can take rides smoothly."});
        
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        return true;
      } else {
        return false;
      }
    } catch (err) {return err;}
  }

  initiateRide(rideCode) {
    // Pass the ride code to LightLine service
    this.service_api.howmuch(this.user_token, rideCode)
    .then(response => {
      if (response.success) {
        if (response.data.amount > 0) {
          // Call lightning network API with amount
          // Listen for payment confirmation
          // response.data.payment_request
        }
      }
    });
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
