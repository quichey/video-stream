FROM mysql:oraclelinux9


# Set the command to start the MySQL server in the foreground
CMD ["mysqld"]


## this one fails on microdnf not existing
# maybe just install yum