//# 유튜브강의 소스
module.exports={
  devServer: {
      proxy: {
        '/api' : {
          target: 'http://localhost:8080'//,
          // changeOrigin: true,
          // pathRewrite: {
          //   '^/': ''
          //}
        }
      }
  }
} 


//#Vue3.js sample code
// const target = 'http://localhost:8080';

// module.exports={
//     devServer: {


//       port: 3000,
//         proxy: {
//             //proxy 요청을 보낼 api 시작 부분
//             '^/api': {
//               target,
//                 changeOrigin: true
//             }
//         }
//     }
// } 

