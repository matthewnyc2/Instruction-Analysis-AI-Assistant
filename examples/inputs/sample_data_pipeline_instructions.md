# Sample Project: Data Processing Pipeline

## Objective
Create a data processing pipeline that ingests CSV files, transforms the data, and outputs to a database.

## Steps
1. Read CSV file from input directory
2. Validate data format
3. Clean and transform data (depends on T002)
4. Calculate statistics || parallel processing
5. Store results in database (depends on T003, T004)
6. Generate report

## Input Specifications
- CSV files with columns: id, name, value, timestamp
- Files can be up to 1GB in size
- Multiple files may arrive simultaneously

## Output Requirements
- Store in PostgreSQL database
- Include error logs for invalid records
- Generate summary report in JSON format

## Performance Requirements
- Process files within 5 minutes
- Handle up to 1 million records per file
- Support parallel processing of multiple files

## Error Handling
- Log all errors with timestamps
- Continue processing valid records even if some are invalid
- Send notification if processing fails
