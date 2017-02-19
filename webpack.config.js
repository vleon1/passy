const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const BundleTracker = require('webpack-bundle-tracker');

const outputPath = path.resolve('./passy/assets/dist/');

const config = {
    entry: './passy/assets/js/index.js',
    output: {
        path: outputPath,
        filename: "bundle.js",
        libraryTarget: 'var',
        library: 'Passy',
    },
    module: {
        rules: [
            { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    use: 'css-loader',
                })
            },
            { test: /\.(svg|ttf|woff|woff2|eot)$/, loader: 'file-loader' },
        ],
    },
    plugins: [
        new CleanWebpackPlugin([outputPath]),
        new webpack.optimize.UglifyJsPlugin(),
        new webpack.ProvidePlugin({
            jQuery: 'jquery',
            $: 'jquery'
        }),
        new ExtractTextPlugin("bundle.css"),
        new BundleTracker({filename: './webpack-stats.json'}),
    ],
    devtool: '#inline-source-map',
};

module.exports = config;
