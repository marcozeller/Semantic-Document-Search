<script lang="ts">
	import { RangeSlider } from '@skeletonlabs/skeleton';
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
	import type { TableSource } from '@skeletonlabs/skeleton';

	let value = 6;
	let max = 25;

	const sourceData = [
		{
			position: 1,
			document: 'Foxes',
			sentence_number: 42,
			sentence_content: 'The little fox jumbed over the fence.'
		},
		{
			position: 2,
			document: 'Lorem Ipsum',
			sentence_number: 1,
			sentence_content:
				'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
		},
		{
			position: 3,
			document: 'Lorem Ipsum',
			sentence_number: 2,
			sentence_content:
				'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
		},
		{
			position: 4,
			document: 'Lorem Ipsum',
			sentence_number: 3,
			sentence_content:
				'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
		},
		{
			position: 5,
			document: 'Wikipedia - Language Model',
			sentence_number: 1,
			sentence_content: 'A language model is a probabilistic model of a natural language.'
		},
		{
			position: 6,
			document: 'Wikipedia - Language Model',
			sentence_number: 101,
			sentence_content:
				'As autoregressive language models, they work by taking an input text and repeatedly predicting the next token or word.'
		}
	];

	const tableSimple: TableSource = {
		// A list of heading labels.
		head: ['Document', 'Sequence Number', 'Sentence Content'],
		// The data visibly shown in your table body UI.
		body: tableMapperValues(sourceData, ['document', 'sentence_number', 'sentence_content']),
		// Optional: The data returned when interactive is enabled and a row is clicked.
		meta: tableMapperValues(sourceData, ['position', 'name', 'symbol', 'weight'])
		// Optional: A list of footer labels.
		//foot: ['Total', '', '<code class="code">6</code>']
	};
</script>

<h1>Search for semantically similar sentences in the corpus:</h1>
<textarea class="textarea" rows="4" placeholder="Enter your sentence here." />

<div class="flex">
	<div class="grow">
		<RangeSlider name="range-slider" bind:value max={25} step={1} ticked>
			<div class="flex justify-between items-center">
				<div class="font-bold">Show number of closest results</div>
				<div class="text-xs">{value} / {max}</div>
			</div>
		</RangeSlider>
	</div>
<button type="button" class="btn variant-filled">Find Results</button>
</div>


<Table class="table-interactive" source={tableSimple} />
