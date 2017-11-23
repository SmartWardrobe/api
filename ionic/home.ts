/* src/pages/home (src klasörünün içerisindeki pages ın home kısmında) */

import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import {Http,Headers} from '@angular/http';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {
 data:any = {};
 
 constructor(public navCtrl: NavController, public http: Http){
 this.data.username = '';
 this.data.response = '';

 this.http = http;
 }

 submit() {
 var link = 'http://localhost:5000/api/user/';
 var mydata = JSON.stringfy({username: this.data.username});

 this.http.post(link, mydata)
  .subscribe(data => {
      this.data.response = data["_body"];

  }, error => {

  console.log("Oooops!");
  })


  }
}
