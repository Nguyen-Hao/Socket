create database CoronaData
go

use CoronaData
go

create table CoronaData (
	country BIGINT not null,
    cases BIGINT not null,
    todayCases BIGINT not null,
    deaths BIGINT not null,
    todayDeaths BIGINT not null,
    recovered BIGINT not null,
    active BIGINT not null,
    critical BIGINT not null,
    casesPerOneMillion BIGINT not null,
    deathsPerOneMillion BIGINT not null,
    totalTests BIGINT not null,
    testsPerOneMillion BIGINT not null,
)
go
