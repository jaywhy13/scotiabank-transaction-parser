<template>
    <div class="row">
        <h2 v-text="name"></h2>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Transaction</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="transaction in transactions" v-bind:key="transaction.description">
                    <td v-text="transaction.date">
                    </td>
                    <td v-text="transaction.description"></td>
                    <td v-text="transaction.amount"></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
