module.exports ={
    "root": true,
    "env": {
      "node": false,
      'browser':true,
      'es6':true
    },
    "extends": [
      "plugin:vue/essential",
      "eslint:prettier/recommended",
    ],
    "parserOptions": {
      "parser": "babel-eslint"
    },
    "rules": {
      "no-console": 0,
      "prettier/prettier": [
        "error",
        {
          "singleQuote": true,
          "trailingComma": "none",
          "bracketSpacing": true,
          "jsxBracketSameLine": true,
          "parser": "flow"
        }
      ]
    }
    
}