import { RouterModule, Routes } from '@angular/router';
import { SignupComponent } from './auth/signup/signup.component';
import { SigninComponent } from './auth/signin/signin.component';
import { SearchComponent } from './main/search/search.component';
import { NgModule } from '@angular/core';

export const routes: Routes = [
    { path: '', component: SignupComponent},
    { path: 'signin', component: SigninComponent},
    { path: 'searchbypostalcode', component: SearchComponent},
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
  export class AppRoutingModule {}