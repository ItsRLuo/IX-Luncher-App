import { Component } from '@angular/core';
import { IXLuncApi } from "../../common/ix-lunch-api.service"
import { LoadingController, NavController } from 'ionic-angular'


 
 @Component({
   selector: 'page-about',
   templateUrl: 'about.html'
 })
 export class AboutPage {
       topTen : any
  constructor(public navCtrl: NavController,
   public eliteApi: IXLuncApi, public loadingController: LoadingController) {}
 
  ionViewDidLoad(){
    //this.geolocate() a
    console.log("As")
    // this.eliteApi.getRating(this.topTen);
    let loader = this.loadingController.create({
      content: 'Getting top rated...'
      //spinner: 'dots'
    });
 
    loader.present().then(() => {
      this.eliteApi.getTopRated().then(data => {
        this.topTen = [data]
        console.log(JSON.stringify(this.topTen))
        loader.dismiss()
      });
    });
    
   }
 }
